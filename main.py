"""Entry point: orchestrates dom, physics, plot, state, and ui packages.

Usage:
    python main.py                            # GUI
    python main.py --seed 42                  # GUI with reproducible layout
    python main.py --headless                 # single headless run, saves NPZ
    python main.py --sweep                    # full parameter sweep
    python main.py --sweep --dry-run          # preview sweep combinations
    python main.py --sweep --max-runs 10 --shuffle
"""

import argparse
import sys

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
from handlers.headless import run_headless
from handlers.sweep import run_sweep
from handlers.sweep.params import FIXED as SWEEP_FIXED
from handlers.dom.seed_zettelkasten import seed_from_zettelkasten
from handlers.state import zettelkasten_path as _zk_path

_SLIDER_KEYS: tuple[str, ...] = ("gravity_ratio", "repel_ratio", "k_edge")


def _list_gpus() -> None:
    try:
        import pynvml  # type: ignore[import-untyped]

        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        for i in range(count):
            h = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(h)
            mem = pynvml.nvmlDeviceGetMemoryInfo(h)
            print(
                f"  [{i}] {name}  "
                f"({int(mem.free)//1024**2} / {int(mem.total)//1024**2} MB free)"
            )
    except Exception:
        try:
            import cupy as cp  # type: ignore[import-untyped]

            count = cp.cuda.runtime.getDeviceCount()
            for i in range(count):
                props = cp.cuda.runtime.getDeviceProperties(i)
                print(
                    f"  [{i}] {props['name'].decode()}  "
                    f"({int(props['totalGlobalMem'])//1024**2} MB total)"
                )
        except Exception:
            print("No CUDA devices found or CuPy/pynvml not available.")


def _apply_overrides(args: argparse.Namespace) -> None:
    if args.cuda_device is not None:
        config.tick.cuda_device = args.cuda_device
        config.simulation.use_gpu = True
    if args.gpu:
        config.simulation.use_gpu = True
    if args.cpu:
        config.simulation.use_gpu = False

    _overrides: list[tuple[object, str, str]] = [
        (config.simulation, "node_count", "node_count"),
        (config.simulation, "dims", "dims"),
        (config.simulation, "weight_min", "weight_min"),
        (config.simulation, "weight_max", "weight_max"),
        (config.simulation, "max_degree", "max_degree"),
        (config.physics, "gravity_ratio", "gravity_ratio"),
        (config.physics, "repel_ratio", "repel_ratio"),
        (config.physics, "k_edge", "k_edge"),
        (config.physics, "initial_temperature", "initial_temp"),
        (config.physics, "cooling_factor", "cooling_factor"),
        (config.tick, "dt", "dt"),
    ]
    for cfg_obj, cfg_attr, args_attr in _overrides:
        value = getattr(args, args_attr, None)
        if value is not None:
            setattr(cfg_obj, cfg_attr, value)


def main() -> None:
    parser = argparse.ArgumentParser(description="3D physics simulation of nodes.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for numpy RNG. Same seed produces the same initial layout.",
    )
    # Mode flags
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without GUI; saves NPZ output and exits.",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run a parameter sweep; spawns one headless subprocess per grid combo.",
    )
    # Shared run options
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Output directory. Headless default: output/  Sweep default: .output/grid",
    )
    parser.add_argument(
        "--max-ticks",
        type=int,
        default=None,
        help="Max physics steps per run. Headless default: 50000  Sweep default: 10000",
    )
    # Sweep-only options
    parser.add_argument(
        "--max-runs",
        type=int,
        default=None,
        help="Cap the sweep grid at N randomly sampled combinations.",
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Randomize sweep run order (useful with --max-runs).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print all sweep combinations and exit without running.",
    )
    # Config overrides (applied before seeding; passed through to subprocesses in sweep mode)
    parser.add_argument(
        "--node-count",
        type=int,
        default=None,
        help="Override config.simulation.node_count",
    )
    parser.add_argument(
        "--dims", type=int, default=None, help="Override config.simulation.dims"
    )
    parser.add_argument(
        "--gravity-ratio",
        type=float,
        default=None,
        help="Override config.physics.gravity_ratio",
    )
    parser.add_argument(
        "--repel-ratio",
        type=float,
        default=None,
        help="Override config.physics.repel_ratio",
    )
    parser.add_argument(
        "--k-edge", type=float, default=None, help="Override config.physics.k_edge"
    )
    parser.add_argument(
        "--initial-temp",
        type=float,
        default=None,
        help="Override config.physics.initial_temperature",
    )
    parser.add_argument(
        "--cooling-factor",
        type=float,
        default=None,
        help="Override config.physics.cooling_factor",
    )
    parser.add_argument(
        "--dt", type=float, default=None, help="Override config.tick.dt"
    )
    parser.add_argument(
        "--weight-min",
        type=float,
        default=None,
        help="Override config.simulation.weight_min",
    )
    parser.add_argument(
        "--weight-max",
        type=float,
        default=None,
        help="Override config.simulation.weight_max",
    )
    parser.add_argument(
        "--max-degree",
        type=int,
        default=None,
        help="Override config.simulation.max_degree (max edges per node)",
    )
    # Compute device selection
    parser.add_argument(
        "--cuda-device",
        type=int,
        default=None,
        help="CUDA device index to use for physics (overrides config.tick.cuda_device)",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Force GPU physics using config.tick.cuda_device",
    )
    parser.add_argument(
        "--cpu", action="store_true", help="Force CPU physics (disables GPU)"
    )
    parser.add_argument(
        "--list-gpus", action="store_true", help="Print available CUDA devices and exit"
    )
    parser.add_argument(
        "--zettelkasten",
        metavar="PATH",
        default="Zettelkasten",
        help="Path to Zettelkasten folder of markdown files (default: Zettelkasten)",
    )
    args = parser.parse_args()

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
        _list_gpus()
        sys.exit(0)

    # Validate Zettelkasten path before GPU init so we fail fast with a clear message.
    from pathlib import Path as _Path
    _zk_dir = _Path(args.zettelkasten)
    if not _zk_dir.is_dir() or not any(_zk_dir.rglob('*.md')):
        sys.exit(f"error: no markdown files found in '{args.zettelkasten}' — Zettelkasten notes are required")
    _zk_path.path = args.zettelkasten

    # Apply config overrides before setup_backend reads use_gpu
    _apply_overrides(args)

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
