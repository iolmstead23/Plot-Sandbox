import numpy as np

from ._backend import get_module
from ._forces_cpu import pairwise_repulsion_sparse, scipy_available
from ._forces_gpu import pairwise_repulsion_chunked_gpu


def pairwise_repulsion(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    cutoff: float = 0.0,
    bh_threshold: int,
    bh_theta: float,
    cpu_sparse_threshold: int = 150,
    linlog: bool = False,
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
            linlog=linlog,
        )

    # CPU Barnes-Hut path: O(N log N) for large N on multi-core CPU.
    # LinLog mode is not supported on the Barnes-Hut path; falls through to
    # sparse or dense below when linlog is True.
    from .barneshut import available as _bh_available, repulsion as _bh_repulsion
    if not linlog and n >= bh_threshold and _bh_available() and positions.shape[1] == 3:
        return _bh_repulsion(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius, theta=bh_theta,
        )

    # CPU sparse path: skip pairs beyond cutoff using scipy.spatial.cKDTree.
    if cutoff > 0.0 and n >= cpu_sparse_threshold and scipy_available():
        return pairwise_repulsion_sparse(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius, cutoff=cutoff,
            linlog=linlog,
        )

    # CPU dense fallback — builds (N, N, D) intermediary.
    diff = positions[:, None, :] - positions[None, :, :]  # (N, N, D)
    d = xp.linalg.norm(diff, axis=-1)
    d_safe = xp.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    if linlog:
        # LinLog: k_r * w_j / sqrt(d^2 + sc^2) — radiating-node weight, linear distance.
        # Heavy nodes near center emit strong repulsion; light nodes can't resist
        # (weak gravity) and float outward. Gravity prevents escape to infinity.
        sc2 = soft_core_radius * soft_core_radius
        d_lin = xp.sqrt(d * d + sc2)  # always > 0 since sc > 0
        mag = 1.0 / d_lin
        xp.fill_diagonal(mag, 0.0)
        mass_j = weights[None, :]  # (1, N) — radiating node's weight
        forces = (k_r * mag * mass_j)[..., None] * direction
    else:
        # Standard: k_r * w_i * w_j / (d^2 + sc^2).
        mag = 1.0 / (d_safe * d_safe + soft_core_radius * soft_core_radius)
        xp.fill_diagonal(mag, 0.0)
        mass_pair = weights[:, None] * weights[None, :]
        forces = (k_r * mag * mass_pair)[..., None] * direction

    return forces.sum(axis=1)
