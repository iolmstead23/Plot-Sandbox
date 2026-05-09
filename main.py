"""Entry point: orchestrates dom, physics, plot, state, and ui packages."""

import argparse

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.plot import build_scatter_3d_figure
from packages.state import state
from packages.ui import launch

from handlers import BUTTON_HANDLERS, physics_tick, seed_physics_dom


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

    rng = np.random.default_rng(args.seed)
    seed_physics_dom(rng)

    edges = dom.pairs_within_radius(config.tick.attraction_radius)
    figure, artists = build_scatter_3d_figure(
        dom.positions, dom.sizes, list(dom.labels), edges,
        view_format=vars(config.view),
        plot_style=vars(config.plot),
        title=config.plot.title,
        focus=state.camera_focus,
        depthshade=False,
    )

    physics_params = {
        "k_g": config.physics.k_central,
        "k_r": config.physics.k_repel,
        "k_a": config.physics.k_attract,
        "r0":  config.physics.soft_core_radius,
        "R":   config.tick.attraction_radius,
        "dt":  config.tick.dt,
    }

    launch(
        figure,
        buttons=BUTTON_HANDLERS,
        sample_size=dom.n,
        params=physics_params,
        artists=artists,
        on_ready=lambda app: app.start_tick(physics_tick, interval_ms=config.tick.interval_ms),
        window_title=config.ui.window_title,
        geometry=config.ui.geometry,
        button_width=config.ui.button_width,
        button_padx=config.ui.button_padx,
        button_pady=config.ui.button_pady,
    )


if __name__ == "__main__":
    main()
