import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import relax_step
from packages.plot import project_to_3d, update_scatter_3d

from ..dom import mutate
from ..state import app as app_state, temperature
from . import _callbacks, _params

_callbacks.wire()

_last_tick_time: float = 0.0
_fps: float = 0.0
_tick_ms: float = 0.0
_render_counter: int = 0
# (n_nodes, n_edges) snapshot — detects structural DOM changes between renders.
_last_render_structure: tuple = (-1, -1)


def physics_tick(app) -> None:
    global _last_tick_time, _fps, _tick_ms, _render_counter, _last_render_structure

    tick_start = time.perf_counter()
    app_state.app = app
    mutate.drain()

    converged = False
    if dom.n > 0:
        proposed = relax_step(
            dom.positions,
            dom.weights,
            dom.pinned,
            edges=dom.edges,
            dt=config.tick.dt,
            temperature=temperature.get(),
            params=_params.build(),
        )
        step = proposed - dom.positions
        max_disp = float(np.linalg.norm(step, axis=1).max())
        converged = max_disp < config.tick.equilibrium_threshold
        dom._set_positions(dom.positions + step)

    _render_counter += 1
    render_every = max(1, config.tick.render_every)
    if app.artists is not None and (_render_counter % render_every == 0):
        current_structure = (dom.n, dom.edges.shape[0])
        structure_changed = current_structure != _last_render_structure
        _last_render_structure = current_structure

        update_scatter_3d(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            # Only send label strings on structural changes — avoids allocating
            # a list copy and re-writing text/style on every physics tick.
            labels=list(dom.labels) if structure_changed else None,
            view_format=vars(config.view),
            plot_style=vars(config.plot),
            positions_only=not structure_changed,
        )
        app.canvas.draw_idle()

    temperature.step()

    now = time.perf_counter()
    _tick_ms = (now - tick_start) * 1000.0
    if _last_tick_time > 0.0:
        elapsed = now - _last_tick_time
        _fps = 1.0 / elapsed if elapsed > 0 else 0.0
    _last_tick_time = now

    app.update_banner(dom.n, temperature.get(), fps=_fps, tick_ms=_tick_ms)

    if converged:
        app.stop_tick()
