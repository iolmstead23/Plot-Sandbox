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


def physics_tick(app) -> None:
    global _last_tick_time, _fps, _tick_ms

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
