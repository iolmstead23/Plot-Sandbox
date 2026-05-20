from typing import Any, Callable

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import project_to_3d, update_vispy_scene

from .state import temperature


def reseed(
    app: Any,
    *,
    stop_fn: Callable[[], None],
    start_fn: Callable,
    seed_fn: Callable[[np.random.Generator], None],
) -> None:
    app.stop_tick()
    stop_fn()
    temperature.reset()  # full reset — _on_dom_change only does warm partial reheat
    seed_fn(np.random.default_rng())

    # Update the existing VisPy visuals in-place — no canvas rebuild needed.
    if app.artists is not None:
        update_vispy_scene(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            size_scale=config.render.size_scale,
            node_size_min=config.render.node_size_min,
            node_size_max=config.render.node_size_max,
        )
        app.canvas.update()

    app.set_converged(False)
    app.update_banner(dom.n)
    start_fn(app)
