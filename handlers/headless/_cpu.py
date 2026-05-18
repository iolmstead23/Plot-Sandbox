"""CPU headless loop — runs physics substeps inline until convergence."""

import sys
import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import cool, relax_step


def run_cpu_loop(
    max_iterations: int,
    substeps: int,
    threshold: float,
    dt: float,
    params: dict,
    T: float,
) -> tuple[float, int]:
    """Run CPU physics to convergence. Returns (final_T, converged_at)."""
    converged_at = max_iterations * substeps
    last_report = time.perf_counter()

    for iteration in range(max_iterations):
        prev = dom.positions.copy()
        pos = dom.positions

        for _ in range(substeps):
            pos = relax_step(pos, dom.weights, dom.pinned, edges=dom.edges,
                             dt=dt, temperature=T, params=params)
            T = cool(T, cooling_factor=config.physics.cooling_factor,
                     min_temperature=config.physics.min_temperature)

        max_disp = float(np.linalg.norm(pos - prev, axis=1).max())
        dom._set_positions(pos)

        now = time.perf_counter()
        if now - last_report >= config.tick.headless_progress_interval:
            print(f"  iter={iteration * substeps}  T={T:.4f}  disp={max_disp:.6f}", file=sys.stderr)
            last_report = now

        if max_disp < threshold * substeps:
            converged_at = (iteration + 1) * substeps
            break

    return T, converged_at
