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
from packages.plot import update_scatter_3d

from . import mutate


# Module-level tick state.
_temperature: float = config.physics.initial_temperature
_app                = None   # set each tick so callbacks can restart if paused

# Physics params dict built once from config — passed to relax_step each tick.
_physics_params: dict = {
    "k_central":        config.physics.k_central,
    "k_repel":          config.physics.k_repel,
    "k_attract":        config.physics.k_attract,
    "soft_core_radius": config.physics.soft_core_radius,
    "max_step":         config.physics.max_step,
    "F_max":            config.physics.F_max,
    "focus":            np.array(config.physics.focus),
}


def reheat() -> None:
    global _temperature
    _temperature = config.physics.initial_temperature


def _on_dom_change(_dom) -> None:
    reheat()


def _on_mutation_enqueued() -> None:
    """Restart the tick when a mutation is queued while the system is paused."""
    if _app is not None and not _app.is_ticking:
        _app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)


# Wire both cascade seams once at import time.
dom.on_change      = _on_dom_change
mutate.on_enqueue  = _on_mutation_enqueued


def physics_tick(app) -> None:
    global _temperature, _app
    _app = app

    # Drain queued mutations before the force computation so array reshapes
    # never race the integrator. Reheat fires automatically via dom.on_change.
    mutate.drain()

    converged = False
    if dom.n > 0:
        new_pos = relax_step(
            dom.positions, dom.weights, dom.pinned,
            dt=config.tick.dt,
            temperature=_temperature,
            params=_physics_params,
        )
        max_disp = float(np.linalg.norm(new_pos - dom.positions, axis=1).max())
        converged = max_disp < config.tick.equilibrium_threshold
        dom._set_positions(new_pos)

    edges = dom.pairs_within_radius(config.tick.attraction_radius)
    if app.artists is not None:
        update_scatter_3d(
            app.artists,
            dom.positions,
            dom.sizes,
            edges,
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
