import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import project_to_3d, update_vispy_scene

from .dom import seed_physics_dom
from .tick import physics_tick
from .tick import thread as _thread


def reseed(app) -> None:
    app.stop_tick()
    _thread.stop()
    seed_physics_dom(np.random.default_rng())

    # Update the existing VisPy visuals in-place — no canvas rebuild needed.
    if app.artists is not None:
        update_vispy_scene(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            labels=list(dom.labels),
            size_scale=config.plot.size_scale,
        )
        app.canvas.update()

    app.update_banner(dom.n)
    app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)
