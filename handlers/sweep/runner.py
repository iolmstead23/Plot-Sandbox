"""Run execution subhandler — drives the per-combo subprocess loop."""

import pathlib
import subprocess
import sys
import time
from typing import Any

import numpy as np


def _build_cmd(
    fixed: dict[str, str],
    param_names: list[str],
    combo: tuple[str, ...],
) -> list[str]:
    merged = {**fixed, **dict(zip(param_names, combo))}
    cmd = [sys.executable, "main.py", "--headless"]
    for flag, value in merged.items():
        cmd += [flag, value]
    return cmd


def _parse_saved_path(stderr: str) -> pathlib.Path | None:
    for line in stderr.splitlines():
        if line.startswith("saved:"):
            return pathlib.Path(line.split()[1])
    return None


def _eta(elapsed: float, done: int, total: int) -> str:
    if done == 0:
        return "--:--"
    rate = elapsed / done
    remaining = rate * (total - done)
    m, s = divmod(int(remaining), 60)
    return f"{m}:{s:02d}"


def _summarize(path: pathlib.Path, max_ticks: int) -> dict[str, Any]:
    d = np.load(path)
    pos = d["positions"]
    w   = d["weights"]
    e   = d["edges"]

    ticks = int(d["ticks"])
    center = pos.mean(axis=0)
    spread = np.linalg.norm(pos - center, axis=1)

    deg = np.zeros(pos.shape[0], dtype=int)
    for i, j in e:
        deg[i] += 1
        deg[j] += 1

    return {
        "nodes":       pos.shape[0],
        "dims":        pos.shape[1],
        "edges":       e.shape[0],
        "ticks":       ticks,
        "converged":   ticks < max_ticks,
        "final_T":     float(d["temperature"]),
        "w_min":       float(w.min()),
        "w_max":       float(w.max()),
        "w_mean":      float(w.mean()),
        "spread_mean": float(spread.mean()),
        "spread_max":  float(spread.max()),
        "deg_mean":    float(deg.mean()),
        "deg_max":     int(deg.max()),
    }


def run_all(
    combos: list[tuple[str, ...]],
    param_names: list[str],
    fixed: dict[str, str],
    max_ticks: int,
) -> tuple[list[dict], list[int]]:
    """Execute one headless simulation subprocess per combo.

    Returns (results, failed_indices) where results holds per-run dicts with
    keys: run_id, params, npz_path, stats, elapsed_s.
    """
    results: list[dict] = []
    failed:  list[int]  = []
    total = len(combos)
    t_sweep = time.perf_counter()

    for idx, combo in enumerate(combos, 1):
        params  = dict(zip(param_names, combo))
        cmd     = _build_cmd(fixed, param_names, combo)

        short_params = "  ".join(
            f"{''.join(w[0] for w in p.lstrip('-').split('-'))}={v}"
            for p, v in params.items()
        )
        eta_str = _eta(time.perf_counter() - t_sweep, idx - 1, total)
        print(f"[{idx:>{len(str(total))}}/{total}]  {short_params}  (eta {eta_str})",
              end="  ", flush=True)

        t0 = time.perf_counter()
        proc = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.perf_counter() - t0

        if proc.returncode != 0:
            print(f"FAILED ({elapsed:.1f}s)")
            snippet = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""
            if snippet:
                print(f"         {snippet[:100]}")
            failed.append(idx)
            continue

        npz_path = _parse_saved_path(proc.stderr)
        if npz_path is None:
            print(f"FAILED — NPZ not found ({elapsed:.1f}s)")
            failed.append(idx)
            continue
        npz_path.parent.mkdir(parents=True, exist_ok=True)
        if not npz_path.exists():
            print(f"FAILED — NPZ not found ({elapsed:.1f}s)")
            failed.append(idx)
            continue

        stats = _summarize(npz_path, max_ticks)
        conv  = "Y" if stats["converged"] else "N"
        print(f"ok  ticks={stats['ticks']:>6}  T={stats['final_T']:.5f}  conv={conv}  ({elapsed:.1f}s)")

        results.append({
            "run_id":    idx,
            "params":    params,
            "npz_path":  npz_path,
            "stats":     stats,
            "elapsed_s": elapsed,
        })

    return results, failed
