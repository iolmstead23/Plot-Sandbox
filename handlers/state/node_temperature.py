"""Per-node heat multiplier for targeted mutation reheating.

Heat values are multiplicative on top of the global temperature scalar:
  effective_temp_i = global_temperature * heat[i]

A value of 1.0 means no boost — the node runs at the global temperature.
Values > 1.0 add extra warmth so recently mutated nodes re-anneal while
the rest of the graph remains settled.

Decay drives all values back toward 1.0 each tick. Nodes far from a
mutation site reach 1.0 quickly; nodes that were just heated stay warm
for proportionally longer.
"""

from __future__ import annotations

import numpy as np

_heat: np.ndarray = np.ones(0, dtype=np.float64)


def init(n: int) -> None:
    global _heat
    _heat = np.ones(n, dtype=np.float64)


def get_array() -> np.ndarray:
    return _heat


def resize(n_new: int) -> None:
    global _heat
    current = _heat.shape[0]
    if n_new == current:
        return
    if n_new > current:
        extra = np.ones(n_new - current, dtype=np.float64)
        _heat = np.concatenate([_heat, extra])
    else:
        _heat = _heat[:n_new]


def heat_nodes(indices: list[int] | np.ndarray, value: float) -> None:
    """Set heat to `value` for the given node indices (clamped to ≥ 1.0)."""
    if len(_heat) == 0 or len(indices) == 0:
        return
    _heat[indices] = max(value, 1.0)


def decay(cooling_factor: float) -> None:
    """Decay heat toward 1.0 each tick: heat = 1 + (heat - 1) * cooling_factor."""
    global _heat
    _heat = 1.0 + (_heat - 1.0) * cooling_factor
