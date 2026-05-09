"""Entry point: orchestrates dom, physics, plot, state, and ui packages."""

import argparse

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import build_scatter_3d_figure, project_to_3d
from packages.state import state
from packages.ui import launch

from handlers import (
    BUTTON_HANDLERS,
    make_force_slider_callback,
    physics_tick,
    seed_physics_dom,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="3D physics simulation of nodes.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for numpy RNG. Same seed produces the same initial layout.",
    )
    args = parser.parse_args()

    dom.weight_to_size = config.dom.weight_to_size
    dom.dims = config.simulation.dims

    rng = np.random.default_rng(args.seed)
    seed_physics_dom(rng)

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

    sliders = [
        (
            "k_central",
            config.physics.k_central,
            0.0,
            10.0,
            0.1,
            make_force_slider_callback("k_central"),
        ),
        (
            "k_repel",
            config.physics.k_repel,
            0.0,
            50.0,
            0.5,
            make_force_slider_callback("k_repel"),
        ),
        (
            "k_edge",
            config.physics.k_edge,
            0.0,
            1.0,
            0.01,
            make_force_slider_callback("k_edge"),
        ),
    ]

    launch(
        figure,
        buttons=BUTTON_HANDLERS,
        sample_size=dom.n,
        sliders=sliders,
        artists=artists,
        on_ready=lambda app: app.start_tick(
            physics_tick, interval_ms=config.tick.interval_ms
        ),
        window_title=config.ui.window_title,
        geometry=config.ui.geometry,
        button_width=config.ui.button_width,
        button_padx=config.ui.button_padx,
        button_pady=config.ui.button_pady,
    )


if __name__ == "__main__":
    main()
