"""Position-only relaxation integrator with cooling temperature.

No velocities. Each tick: sum forces, cap per-node magnitude, zero pinned
rows, scale by temperature * dt, take a small step. Temperature decays each
frame; the caller bumps it back to initial_temperature after any structural
DOM change so the layout re-settles.

All tunable constants are supplied by the caller via `params` and the
`cooling_factor`/`min_temperature` kwargs — nothing is hardcoded here.
"""

import numpy as np

from .forces import (
    central_gravity,
    edge_attraction,
    pairwise_attraction,
    pairwise_repulsion,
)


def relax_step(
    positions: np.ndarray,
    weights: np.ndarray,
    pinned: np.ndarray,
    *,
    edges: np.ndarray | None = None,
    dt: float,
    temperature: float,
    params: dict,
) -> np.ndarray:
    p = params

    if edges is not None and edges.shape[0] > 0:
        attract = edge_attraction(
            positions,
            edges,
            k_e=p["k_edge"],
            rest_length=p["edge_rest_length"],
        )
    else:
        attract = pairwise_attraction(
            positions,
            weights,
            k_a=p["k_attract"],
            soft_core_radius=p["soft_core_radius"],
        )

    F = (
        central_gravity(
            positions,
            weights,
            k_g=p["k_central"],
            focus=p["focus"],
            soft_core_radius=p["soft_core_radius"],
        )
        + pairwise_repulsion(
            positions, weights,
            k_r=p["k_repel"],
            soft_core_radius=p["soft_core_radius"],
            cutoff=p.get("repulsion_cutoff", 0.0),
        )
        + attract
    )

    # Per-node cap on force magnitude (preserves direction, bounds blow-ups).
    norms = np.linalg.norm(F, axis=1, keepdims=True)
    scale = np.minimum(1.0, p["F_max"] / np.where(norms > 0.0, norms, 1.0))
    F = F * scale

    F[pinned] = 0.0

    step = F * dt * temperature
    # Cap step magnitude per node, preserving direction. Per-axis clipping
    # would distort direction whenever a single component saturates and is
    # a known cause of jitter near equilibrium.
    step_norms = np.linalg.norm(step, axis=1, keepdims=True)
    step_scale = np.minimum(
        1.0, p["max_step"] / np.where(step_norms > 0.0, step_norms, 1.0)
    )
    step = step * step_scale
    return positions + step


def cool(
    temperature: float,
    *,
    cooling_factor: float,
    min_temperature: float,
) -> float:
    return max(min_temperature, temperature * cooling_factor)
