"""Physics tick: orchestrator that bridges DOM <-> physics <-> renderer.

Per CLAUDE.md, packages cannot import each other; only handlers and main may
compose them. This is where physics meets DOM. Pure NumPy `relax_step` lives
in packages/physics; here we read DOM arrays, integrate, write back, and
update the renderer artists in place.
"""

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import cool, relax_step
from packages.plot import project_to_3d, update_scatter_3d

from . import mutate

# Module-level tick state.
_temperature: float = config.physics.initial_temperature
_app = None  # set each tick so callbacks can restart if paused
_prev_step: np.ndarray | None = None  # cached step for momentum-style smoothing

# Focus is a (dims,) vector; pad the configured 3-vector with zeros for dims > 3.
_focus = np.zeros(config.simulation.dims, dtype=np.float64)
_focus[: min(3, config.simulation.dims)] = np.asarray(
    config.physics.focus, dtype=np.float64
)[: min(3, config.simulation.dims)]


def _build_physics_params() -> dict:
    # Built per tick so live edits to config.physics (e.g. via the UI sliders)
    # take effect on the next step without any cache invalidation plumbing.
    p = config.physics
    return {
        "k_central": p.k_central,
        "k_repel": p.k_repel,
        "k_attract": p.k_attract,
        "k_edge": p.k_edge,
        "soft_core_radius": p.soft_core_radius,
        "max_step": p.max_step,
        "F_max": p.F_max,
        "focus": _focus,
    }


def reheat() -> None:
    global _temperature, _prev_step
    _temperature = config.physics.initial_temperature
    # Drop momentum on a reheat so a structural mutation doesn't carry stale
    # velocity from the prior topology into the new one.
    _prev_step = None


def _on_dom_change(_dom) -> None:
    reheat()


def _on_mutation_enqueued() -> None:
    """Restart the tick when a mutation is queued while the system is paused."""
    if _app is not None and not _app.is_ticking:
        _app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)


# Wire both cascade seams once at import time.
dom.on_change = _on_dom_change
mutate.on_enqueue = _on_mutation_enqueued


def physics_tick(app) -> None:
    global _temperature, _app, _prev_step
    _app = app

    # Drain queued mutations before the force computation so array reshapes
    # never race the integrator. Reheat fires automatically via dom.on_change.
    mutate.drain()

    converged = False
    if dom.n > 0:
        new_pos = relax_step(
            dom.positions,
            dom.weights,
            dom.pinned,
            edges=dom.edges,
            dt=config.tick.dt,
            temperature=_temperature,
            params=_build_physics_params(),
        )
        proposed_step = new_pos - dom.positions

        # Momentum-style smoothing: blend with the previous step so frame-to-
        # frame motion is visually continuous and not jittery near equilibrium.
        # Reset whenever the array shape changed (add/remove node).
        damping = config.physics.damping
        if (
            _prev_step is not None
            and _prev_step.shape == proposed_step.shape
            and damping > 0.0
        ):
            smoothed_step = (1.0 - damping) * proposed_step + damping * _prev_step
        else:
            smoothed_step = proposed_step
        _prev_step = smoothed_step

        final_pos = dom.positions + smoothed_step
        max_disp = float(np.linalg.norm(smoothed_step, axis=1).max())
        converged = max_disp < config.tick.equilibrium_threshold
        dom._set_positions(final_pos)

    if app.artists is not None:
        update_scatter_3d(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            labels=list(dom.labels),
            view_format=vars(config.view),
            plot_style=vars(config.plot),
        )
        app.canvas.draw_idle()

    _temperature = cool(
        _temperature,
        cooling_factor=config.physics.cooling_factor,
        min_temperature=config.physics.min_temperature,
    )
    app.update_banner(dom.n, _temperature)

    if converged:
        app.stop_tick()
