"""CPU headless loop — runs physics substeps inline until convergence."""

import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import cool, relax_step
from .. import stats as _stats


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
    max_steps = max_iterations * substeps
    _stats.reset()
    iter_t0 = time.perf_counter()

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

        steps_done = (iteration + 1) * substeps
        iter_elapsed = time.perf_counter() - iter_t0
        sps = steps_done / iter_elapsed if iter_elapsed > 0 else 0.0
        _stats.maybe_cpu(
            sps, T, steps_done,
            config.tick.stats_interval, max_steps,
        )

        if max_disp < threshold * substeps:
            converged_at = steps_done
            break

    return T, converged_at
