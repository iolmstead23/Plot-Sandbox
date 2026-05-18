"""GPU headless loop — runs physics substeps on device until convergence."""

import sys
import time

import numpy as np

from packages.config import config
from packages.physics import cool, relax_step, to_numpy


def run_gpu_loop(
    pos,
    w,
    pin,
    e,
    max_iterations: int,
    substeps: int,
    threshold: float,
    dt: float,
    params: dict,
    T: float,
) -> tuple[np.ndarray, float, int]:
    """Run GPU physics to convergence. Returns (positions_np, final_T, converged_at)."""
    converged_at = max_iterations * substeps
    last_report = time.perf_counter()

    for iteration in range(max_iterations):
        prev = pos.copy()

        for _ in range(substeps):
            pos = relax_step(pos, w, pin, edges=e, dt=dt, temperature=T, params=params)
            T = cool(T, cooling_factor=config.physics.cooling_factor,
                     min_temperature=config.physics.min_temperature)

        try:
            import cupy as cp
            max_disp = float(cp.max(cp.linalg.norm(pos - prev, axis=1)).get())
        except Exception:
            max_disp = float(np.linalg.norm(
                to_numpy(pos).astype(np.float64) - to_numpy(prev).astype(np.float64),
                axis=1).max())

        now = time.perf_counter()
        if now - last_report >= config.tick.headless_progress_interval:
            print(f"  iter={iteration * substeps}  T={T:.4f}  disp={max_disp:.6f}", file=sys.stderr)
            last_report = now

        if max_disp < threshold * substeps:
            converged_at = (iteration + 1) * substeps
            break

    return to_numpy(pos).astype(np.float64), T, converged_at
