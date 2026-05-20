import argparse
import sys

from packages.config import config


def list_gpus() -> None:
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


def apply_overrides(args: argparse.Namespace) -> None:
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


def build_arg_parser() -> argparse.ArgumentParser:
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
    return parser


__all__ = ["build_arg_parser", "list_gpus", "apply_overrides"]
