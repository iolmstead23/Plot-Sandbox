"""Entry point: orchestrates dom, physics, plot, state, and ui packages."""

import argparse

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import setup_backend
from packages.plot import build_vispy_scene, project_to_3d
from packages.state import state
from packages.ui import launch

from handlers import (
    BUTTON_HANDLERS,
    make_force_slider_callback,
    physics_tick,
    reseed_handler,
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

    setup_backend(config.simulation.use_gpu)

    dom.weight_to_size = config.dom.weight_to_size
    dom.dims = config.simulation.dims

    rng = np.random.default_rng(args.seed)
    seed_physics_dom(rng)

    scene_objects = build_vispy_scene(
        project_to_3d(dom.positions),
        dom.sizes,
        list(dom.labels),
        dom.edges,
        title=config.plot.title,
        focus=state.camera_focus,
        elev=config.view.elev,
        azim=config.view.azim,
        axis_length=config.view.view_range * 0.4,
        size_scale=config.plot.size_scale,
        camera_distance=config.view.camera_distance,
        node_size_min=config.plot.node_size_min,
        node_size_max=config.plot.node_size_max,
    )

    sliders = [
        (
            "gravity_ratio",
            config.physics.gravity_ratio,
            0.0,
            0.01,
            0.0001,
            make_force_slider_callback("gravity_ratio", reseed_fn=reseed_handler),
        ),
        (
            "repel_ratio",
            config.physics.repel_ratio,
            0.0,
            0.05,
            0.0005,
            make_force_slider_callback("repel_ratio", reseed_fn=reseed_handler),
        ),
        (
            "k_edge",
            config.physics.k_edge,
            0.0,
            1.0,
            0.01,
            make_force_slider_callback("k_edge", reseed_fn=reseed_handler),
        ),
    ]

    launch(
        scene_objects,
        buttons=BUTTON_HANDLERS,
        sample_size=dom.n,
        sliders=sliders,
        on_ready=lambda app: app.start_tick(
            physics_tick, interval_ms=config.tick.interval_ms
        ),
        window_title=config.ui.window_title,
        geometry=config.ui.geometry,
        button_padx=config.ui.button_padx,
        button_pady=config.ui.button_pady,
    )


if __name__ == "__main__":
    main()
