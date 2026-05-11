import numpy as np

from ._backend import get_module
from ._forces_cpu import pairwise_attraction_sparse_cpu, scipy_available
from ._forces_gpu import pairwise_attraction_chunked_gpu


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
