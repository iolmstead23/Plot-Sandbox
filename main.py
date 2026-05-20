"""Entry point: orchestrates dom, physics, plot, state, and ui packages.

Usage:
    python main.py                            # GUI
    python main.py --seed 42                  # GUI with reproducible layout
    python main.py --headless                 # single headless run, saves NPZ
    python main.py --sweep                    # full parameter sweep
    python main.py --sweep --dry-run          # preview sweep combinations
    python main.py --sweep --max-runs 10 --shuffle
"""

import sys
from pathlib import Path

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import setup_backend
from packages.plot import build_vispy_scene, project_to_3d
from packages.state import state
from packages.ui import SliderSpec, launch

from handlers import (
    BUTTON_HANDLERS,
    make_force_slider_callback,
    physics_tick,
    reseed_handler,
)
from handlers.cli import apply_overrides, build_arg_parser, list_gpus
from handlers.headless import run_headless
from handlers.sweep import run_sweep
from handlers.sweep.params import FIXED as SWEEP_FIXED
from handlers.dom.seed_zettelkasten import seed_from_zettelkasten
from handlers.state import zettelkasten_path as _zk_path

_SLIDER_KEYS: tuple[str, ...] = ("gravity_ratio", "repel_ratio", "k_edge")


def main() -> None:
    args = build_arg_parser().parse_args()

    # Sweep mode: build fixed dict from SWEEP_FIXED + CLI overrides, dispatch, and exit.
    # No GPU init needed here — each subprocess calls setup_backend for itself.
    if args.sweep:
        fixed = {
            **SWEEP_FIXED,
            **{
                k: str(v)
                for k, v in {
                    "--output-dir": args.output_dir,
                    "--max-ticks": args.max_ticks,
                    "--seed": args.seed,
                    "--node-count": args.node_count,
                }.items()
                if v is not None
            },
        }
        run_sweep(fixed, args)
        sys.exit(0)

    # --list-gpus: enumerate CUDA devices and exit
    if args.list_gpus:
        list_gpus()
        sys.exit(0)

    # Validate Zettelkasten path before GPU init so we fail fast with a clear message.
    _zk_dir = Path(args.zettelkasten)
    if not _zk_dir.is_dir() or not any(_zk_dir.rglob("*.md")):
        sys.exit(
            f"error: no markdown files found in '{args.zettelkasten}' — Zettelkasten notes are required"
        )
    _zk_path.path = args.zettelkasten

    # Apply config overrides before setup_backend reads use_gpu
    apply_overrides(args)

    setup_backend(
        config.simulation.use_gpu,
        cuda_device=config.tick.cuda_device,
        gpu_memory_pool_gb=config.simulation.gpu_memory_pool_gb,
    )

    rng = np.random.default_rng(args.seed)

    if args.headless:
        run_headless(
            args.output_dir or "output",
            rng,
            args.max_ticks or config.tick.headless_max_ticks,
            seed_fn=lambda rng: seed_from_zettelkasten(args.zettelkasten, rng),
        )
        sys.exit(0)

    dom.weight_to_size = config.render.weight_to_size
    dom.dims = config.simulation.dims

    seed_from_zettelkasten(args.zettelkasten, rng)

    scene_objects = build_vispy_scene(
        project_to_3d(dom.positions),
        dom.sizes,
        dom.edges,
        title=config.render.title,
        focus=state.camera_focus,
        elev=config.render.camera_elev,
        azim=config.render.camera_azim,
        axis_length=config.render.view_range * 0.4,
        size_scale=config.render.size_scale,
        camera_distance=config.render.camera_distance,
        node_size_min=config.render.node_size_min,
        node_size_max=config.render.node_size_max,
    )

    sr = config.sliders
    sliders: list[SliderSpec] = [
        (
            key,
            getattr(config.physics, key),
            getattr(sr, key).min,
            getattr(sr, key).max,
            getattr(sr, key).step,
            make_force_slider_callback(key, reseed_fn=reseed_handler),
        )
        for key in _SLIDER_KEYS
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
