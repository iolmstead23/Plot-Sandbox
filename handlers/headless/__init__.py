"""Headless simulation handler — runs physics to convergence without a GUI."""

import pathlib
import secrets
import sys
import time
from datetime import datetime

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import is_gpu, to_device

from ..dom.seed import seed_physics_dom
from ..state import temperature
from ..tick._params import build as _build_params
from ._cpu import run_cpu_loop
from ._gpu import run_gpu_loop


def _make_run_dir(base_dir: str) -> pathlib.Path:
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + secrets.token_hex(3)
    run_dir = pathlib.Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _save_npz(run_dir: pathlib.Path, converged_at: int, T: float) -> pathlib.Path:
    output_path = run_dir / "sim.npz"
    np.savez_compressed(
        output_path,
        positions=dom.positions,
        weights=dom.weights,
        edges=dom.edges,
        ticks=np.array(converged_at),
        temperature=np.array(T),
    )
    return output_path


def run_headless(
    output_dir: str, rng: np.random.Generator, max_ticks: int = 50_000
) -> None:
    run_dir = _make_run_dir(output_dir)
    dom.weight_to_size = config.render.weight_to_size
    dom.dims = config.simulation.dims
    seed_physics_dom(rng)
    temperature.reset()

    substeps = max(1, config.tick.physics_substeps)
    threshold = config.tick.equilibrium_threshold
    dt = config.tick.dt
    params = _build_params()
    T = temperature.get()
    max_iterations = max(1, max_ticks // substeps)

    print(
        f"headless: n={dom.n}  dims={dom.dims}  gpu={is_gpu()}  substeps={substeps}",
        file=sys.stderr,
    )
    t_start = time.perf_counter()

    if is_gpu():
        try:
            import cupy as cp

            cp.cuda.Device(config.tick.cuda_device).use()
        except Exception:
            pass

        pos = to_device(dom.positions.astype(np.float32))
        w = to_device(dom.weights.astype(np.float32))
        pin = to_device(dom.pinned.astype(np.uint8))
        e = to_device(dom.edges.astype(np.int32))

        final_positions, T, converged_at = run_gpu_loop(
            pos, w, pin, e, max_iterations, substeps, threshold, dt, params, T
        )
        dom._set_positions(final_positions)
    else:
        T, converged_at = run_cpu_loop(
            max_iterations, substeps, threshold, dt, params, T
        )

    elapsed = time.perf_counter() - t_start
    output_path = _save_npz(run_dir, converged_at, T)
    print(
        f"saved: {output_path}  ticks={converged_at}  elapsed={elapsed:.1f}s",
        file=sys.stderr,
    )
