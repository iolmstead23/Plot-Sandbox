"""Position-only relaxation integrator with cooling temperature.

No velocities. Each tick: sum forces, cap per-node magnitude, zero pinned
rows, scale by temperature * dt, take a small step. Temperature decays each
frame; the caller bumps it back to initial_temperature after any structural
DOM change so the layout re-settles.

All tunable constants are supplied by the caller via `params` and the
`cooling_factor`/`min_temperature` kwargs — nothing is hardcoded here.
"""

import numpy as np

from .forces import central_gravity, pairwise_attraction, pairwise_repulsion


def relax_step(
    positions: np.ndarray,
    weights: np.ndarray,
    pinned: np.ndarray,
    *,
    dt: float,
    temperature: float,
    params: dict,
) -> np.ndarray:
    p = params

    F = (
        central_gravity(positions, weights, k_g=p["k_central"], focus=p["focus"])
        + pairwise_repulsion(positions, weights, k_r=p["k_repel"],
                             soft_core_radius=p["soft_core_radius"])
        + pairwise_attraction(positions, weights, k_a=p["k_attract"],
                              soft_core_radius=p["soft_core_radius"])
    )

    # Per-node cap on force magnitude (preserves direction, bounds blow-ups).
    norms = np.linalg.norm(F, axis=1, keepdims=True)
    scale = np.minimum(1.0, p["F_max"] / np.where(norms > 0.0, norms, 1.0))
    F = F * scale

    F[pinned] = 0.0

    step = F * dt * temperature
    step = np.clip(step, -p["max_step"], p["max_step"])
    return positions + step


def cool(
    temperature: float,
    *,
    cooling_factor: float,
    min_temperature: float,
) -> float:
    return max(min_temperature, temperature * cooling_factor)
