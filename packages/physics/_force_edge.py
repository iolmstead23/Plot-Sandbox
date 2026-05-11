import numpy as np

from ._backend import get_module


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
