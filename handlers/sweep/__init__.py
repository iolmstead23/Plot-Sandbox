"""Sweep handler — orchestrates grid building, execution, and reporting."""

import pathlib
import time

from .grid import prepare_grid
from .params import GRID
from .reporter import report
from .runner import run_all


def run_sweep(fixed: dict[str, str], cli) -> None:
    max_ticks = int(fixed["--max-ticks"])
    out_base = pathlib.Path(fixed["--output-dir"])

    grid_result = prepare_grid(GRID, cli)
    if grid_result is None:
        return

    param_names, combos, total = grid_result
    out_base.mkdir(parents=True, exist_ok=True)
    print(f"\nRunning {total} simulations  ->  {out_base}/\n")

    t_sweep = time.perf_counter()
    results, failed = run_all(combos, param_names, fixed, max_ticks)
    elapsed = time.perf_counter() - t_sweep

    report(results, failed, param_names, out_base, total, elapsed)
