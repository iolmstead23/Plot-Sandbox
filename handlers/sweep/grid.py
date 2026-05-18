"""Grid preparation subhandler — builds, shuffles, subsamples, and previews the run matrix."""

import argparse
import itertools
import math
import random
from typing import Any

import numpy as np


def _expand(spec: list | dict) -> list[str]:
    """Expand a value list or range spec into a list of CLI-ready strings."""
    if isinstance(spec, list):
        return [str(v) for v in spec]

    start: float = spec["start"]
    stop:  float = spec["stop"]
    steps: int   = int(spec["steps"])
    scale: str   = spec.get("scale", "linear")
    dtype: str   = spec.get("dtype", "float")

    if scale == "log":
        if start <= 0 or stop <= 0:
            raise ValueError(f"log scale requires start and stop > 0, got {start}, {stop}")
        vals: Any = np.logspace(math.log10(start), math.log10(stop), steps)
    else:
        vals = np.linspace(start, stop, steps)

    if dtype == "int":
        int_vals = [int(round(v)) for v in vals]
        seen: set[int] = set()
        unique: list[int] = []
        for v in int_vals:
            if v not in seen:
                seen.add(v)
                unique.append(v)
        return [str(v) for v in unique]

    return [f"{float(v):.6g}" for v in vals]


def _build_grid(grid: dict) -> tuple[list[str], list[tuple[str, ...]]]:
    """Return (param_names, list_of_value_tuples) for the full cartesian product."""
    params = list(grid.keys())
    value_lists = [_expand(grid[p]) for p in params]
    combos = list(itertools.product(*value_lists))
    return params, combos


def prepare_grid(
    grid: dict,
    cli: argparse.Namespace,
) -> tuple[list[str], list[tuple[str, ...]], int] | None:
    """Build the run matrix from GRID, apply shuffle/subsample, print dimensions.

    Handles the dry-run path internally — prints the combination table and returns
    None to signal the caller to stop. Returns (param_names, combos, total) otherwise.
    """
    param_names, combos = _build_grid(grid)

    counts = [len(_expand(grid[p])) for p in param_names]
    print("\nGrid dimensions:")
    for p, c in zip(param_names, counts):
        vals = _expand(grid[p])
        print(f"  {p:<20} {c} values: {', '.join(vals)}")
    total_grid = math.prod(counts)
    print(f"\n  Total combinations: {' x '.join(str(c) for c in counts)} = {total_grid}")

    if cli.shuffle or cli.max_runs is not None:
        combos = list(combos)
        random.shuffle(combos)
    if cli.max_runs is not None and cli.max_runs < len(combos):
        combos = combos[: cli.max_runs]
        print(f"  Subsampled to:      {len(combos)} runs (--max-runs)")

    total = len(combos)

    if cli.dry_run:
        _print_dry_run(param_names, combos, total)
        return None

    return param_names, combos, total


def _print_dry_run(
    param_names: list[str],
    combos: list[tuple[str, ...]],
    total: int,
) -> None:
    print(f"\nDry run: {total} combinations\n")
    short = [p.lstrip("-").replace("-", "_") for p in param_names]
    header = "  ".join(f"{s:<14}" for s in short)
    print(f"  {'#':>5}  {header}")
    print(f"  {'-'*5}  {'-'*len(header)}")
    for idx, combo in enumerate(combos, 1):
        row = "  ".join(f"{v:<14}" for v in combo)
        print(f"  {idx:>5}  {row}")
    print()
