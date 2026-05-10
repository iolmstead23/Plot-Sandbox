"""Pure force functions — array-backend-agnostic via _backend.get_module().

Each function resolves its array module (numpy or cupy) from the positions
argument so the same code runs on CPU or GPU without modification.

No imports from other packages. DOM is never referenced here.
"""

import numpy as np

from ._backend import get_module
from ._forces_gpu import pairwise_repulsion_chunked_gpu, pairwise_attraction_chunked_gpu
from ._forces_cpu import scipy_available, pairwise_repulsion_sparse, pairwise_attraction_sparse_cpu


def central_gravity(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_g: float,
    focus: np.ndarray,
    soft_core_radius: float,
) -> np.ndarray:
    xp = get_module(positions)
    # Move focus to the same device as positions (no-op when both CPU).
    focus = xp.asarray(focus)
    # Constant-magnitude inward force, scaled by mass. The soft-core denominator
    # blends to a linear restoring force inside the core radius so nodes that
    # cross the focus do not oscillate indefinitely.
    delta = positions - focus[None, :]
    r_sq = xp.sum(delta * delta, axis=-1, keepdims=True)
    r_soft = xp.sqrt(r_sq + soft_core_radius * soft_core_radius)
    return -k_g * weights[:, None] * (delta / r_soft)


def pairwise_repulsion(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    cutoff: float = 0.0,
) -> np.ndarray:
    xp = get_module(positions)
    n = positions.shape[0]
    if n < 2:
        return xp.zeros_like(positions)

    # GPU: chunked path caps peak VRAM at O(_CHUNK*N*D) instead of O(N^2*D).
    if xp is not np:
        return pairwise_repulsion_chunked_gpu(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius,
        )

    # CPU Barnes-Hut path: O(N log N) for large N on multi-core CPU.
    from .barneshut import BH_THRESHOLD, available as _bh_available, repulsion as _bh_repulsion
    if n >= BH_THRESHOLD and _bh_available() and positions.shape[1] == 3:
        return _bh_repulsion(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius,
        )

    # CPU sparse path: skip pairs beyond cutoff using scipy.spatial.cKDTree.
    if cutoff > 0.0 and n >= 150 and scipy_available():
        return pairwise_repulsion_sparse(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius, cutoff=cutoff,
        )

    # CPU dense fallback — builds (N, N, D) intermediary.
    diff = positions[:, None, :] - positions[None, :, :]  # (N, N, D)
    d = xp.linalg.norm(diff, axis=-1)
    d_safe = xp.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    # Smoothed 1/(d^2 + eps^2): bounded at d=0, C-inf everywhere.
    mag = 1.0 / (d_safe * d_safe + soft_core_radius * soft_core_radius)
    xp.fill_diagonal(mag, 0.0)

    mass_pair = weights[:, None] * weights[None, :]
    forces = (k_r * mag * mass_pair)[..., None] * direction  # (N, N, D)
    return forces.sum(axis=1)


def pairwise_attraction(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
    cutoff: float = 0.0,
) -> np.ndarray:
    xp = get_module(positions)
    n = positions.shape[0]
    if n < 2:
        return xp.zeros_like(positions)

    if xp is not np:
        return pairwise_attraction_chunked_gpu(
            positions, weights, k_a=k_a,
            soft_core_radius=soft_core_radius,
        )

    if cutoff > 0.0 and n >= 150 and scipy_available():
        return pairwise_attraction_sparse_cpu(
            positions, weights, k_a=k_a,
            soft_core_radius=soft_core_radius, cutoff=cutoff,
        )

    # Dense fallback — builds (N, N, D) intermediary.
    diff = positions[None, :, :] - positions[:, None, :]  # j - i, toward j
    d = xp.linalg.norm(diff, axis=-1)
    d_safe = xp.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    flat_mag = 1.0 / (soft_core_radius * soft_core_radius)
    inv_sq = 1.0 / (d_safe * d_safe)
    near = d < soft_core_radius
    mag = xp.where(near, flat_mag, inv_sq)
    xp.fill_diagonal(mag, 0.0)

    mass_pair = weights[:, None] * weights[None, :]
    forces = (k_a * mag * mass_pair)[..., None] * direction
    return forces.sum(axis=1)


def edge_attraction(
    positions: np.ndarray,
    edges: np.ndarray,
    *,
    k_e: float,
    rest_length: float,
) -> np.ndarray:
    """Hooke's Law spring along explicit graph edges.

    F = k_e * (d - L0). Attractive when d > L0, repulsive when d < L0.
    Uses bincount scatter — works on both CPU (numpy) and GPU (cupy).
    """
    xp = get_module(positions)
    n, d = positions.shape
    forces = xp.zeros_like(positions)
    if edges.shape[0] == 0:
        return forces

    i_idx = edges[:, 0]
    j_idx = edges[:, 1]
    diff = positions[j_idx] - positions[i_idx]
    dist = xp.linalg.norm(diff, axis=-1)
    d_safe = xp.where(dist > 0.0, dist, 1.0)
    direction = diff / d_safe[:, None]
    f = (k_e * (dist - rest_length))[:, None] * direction  # (E, D)

    xp.add.at(forces, i_idx, f)
    xp.add.at(forces, j_idx, -f)
    return forces
