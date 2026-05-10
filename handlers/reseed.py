import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import build_scatter_3d_figure, project_to_3d
from packages.state import state

from .dom import seed_physics_dom
from .tick import physics_tick


def reseed(app) -> None:
    app.stop_tick()
    seed_physics_dom(np.random.default_rng())
    figure, artists = build_scatter_3d_figure(
        project_to_3d(dom.positions),
        dom.sizes,
        list(dom.labels),
        dom.edges,
        view_format=vars(config.view),
        plot_style=vars(config.plot),
        title=config.plot.title,
        focus=state.camera_focus,
        depthshade=False,
    )
    app.set_figure(figure)
    app.set_artists(artists)
    app.update_banner(dom.n)
    app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)
