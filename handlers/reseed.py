from typing import Callable

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import project_to_3d, update_vispy_scene

from .dom import seed_physics_dom


def reseed(app, *, stop_fn: Callable[[], None], start_fn: Callable) -> None:
    app.stop_tick()
    stop_fn()
    seed_physics_dom(np.random.default_rng())

    # Update the existing VisPy visuals in-place — no canvas rebuild needed.
    if app.artists is not None:
        update_vispy_scene(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            size_scale=config.plot.size_scale,
        )
        app.canvas.update()

    app.update_banner(dom.n)
    start_fn(app)
