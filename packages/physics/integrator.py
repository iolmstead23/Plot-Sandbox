"""Position-only relaxation integrator — array-backend-agnostic.

No velocities. Each tick: sum forces, cap per-node magnitude, zero pinned
rows, scale by temperature * dt, take a small step. Temperature decays each
frame; the caller bumps it back to initial_temperature after any structural
DOM change so the layout re-settles.

All arrays (positions, weights, pinned, edges) must be on the same device.
The tick handler in handlers/tick/__init__.py is responsible for uploading
them to GPU before calling relax_step and downloading the result back.
"""

import numpy as np

from ._backend import get_module
from ._force_attraction import pairwise_attraction
from ._force_edge import edge_attraction
from ._force_gravity import central_gravity
from ._force_repulsion import pairwise_repulsion
from ._forces_gpu_fused import relax_step_fused_gpu


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
    xp = get_module(positions)

    # GPU + 3-D + edges present: single CUDA kernel handles all forces and
    # integration in one launch, eliminating ~40 CuPy kernel-dispatch calls.
    if (
        xp is not np
        and positions.shape[1] == 3
        and edges is not None
    ):
        return relax_step_fused_gpu(
            positions, weights, pinned,
            edges=edges, dt=dt, temperature=temperature, params=params,
        )

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
            cutoff=p.get("repulsion_cutoff", 0.0),
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
            positions,
            weights,
            k_r=p["k_repel"],
            soft_core_radius=p["soft_core_radius"],
            cutoff=p.get("repulsion_cutoff", 0.0),
            bh_threshold=p["bh_threshold"],
            bh_theta=p["bh_theta"],
            cpu_sparse_threshold=p.get("cpu_sparse_threshold", 150),
        )
        + attract
    )

    # Per-node force magnitude cap — preserves direction, bounds blow-ups.
    norms = xp.linalg.norm(F, axis=1, keepdims=True)
    scale = xp.minimum(1.0, p["F_max"] / xp.where(norms > 0.0, norms, 1.0))
    F = F * scale

    F[pinned] = 0.0

    step = F * dt * temperature
    step_norms = xp.linalg.norm(step, axis=1, keepdims=True)
    step_scale = xp.minimum(
        1.0, p["max_step"] / xp.where(step_norms > 0.0, step_norms, 1.0)
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
