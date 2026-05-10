"""Pure NumPy force functions. Each returns an (N, D) net-force-per-node array.

No imports from other packages. The DOM is never referenced — these are plain
math on arrays. The orchestrator (handlers/tick.py) reads DOM arrays, passes
them in, and writes the integrator output back.
"""

import numpy as np


def central_gravity(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_g: float,
    focus: np.ndarray,
    soft_core_radius: float,
) -> np.ndarray:
    # Constant-magnitude inward force, scaled by mass. Unlike a linear spring,
    # this does not go to zero at the focus. Every node feels the same inward
    # pressure regardless of distance. Repulsion prevents collapse — not the
    # weakening of gravity near the center.
    #
    # The soft-core denominator blends to a linear restoring force inside the
    # core radius. Without this, a node that crosses the focus flips direction
    # each tick and vibrates in place indefinitely.
    delta = positions - focus[None, :]
    r_sq = np.sum(delta * delta, axis=-1, keepdims=True)
    r_soft = np.sqrt(r_sq + soft_core_radius * soft_core_radius)
    return -k_g * weights[:, None] * (delta / r_soft)


_scipy_ok: bool | None = None


def _scipy_available() -> bool:
    global _scipy_ok
    if _scipy_ok is None:
        try:
            import scipy.spatial  # noqa: F401
            _scipy_ok = True
        except ImportError:
            _scipy_ok = False
    return _scipy_ok


def pairwise_repulsion(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    cutoff: float = 0.0,
) -> np.ndarray:
    n = positions.shape[0]
    if n < 2:
        return np.zeros_like(positions)

    # Sparse path: skip pairs beyond `cutoff`. O(N log N + P) vs O(N²).
    # KDTree overhead is worthwhile above ~150 nodes; below that the dense
    # NumPy broadcast is faster due to lower constant factors.
    if cutoff > 0.0 and n >= 150 and _scipy_available():
        return _pairwise_repulsion_sparse(positions, weights, k_r=k_r,
                                          soft_core_radius=soft_core_radius,
                                          cutoff=cutoff)

    # Dense path — allocates (N, N, D). Stays on this path for small N or
    # when scipy is absent.
    diff = positions[:, None, :] - positions[None, :, :]  # (N, N, D)
    d = np.linalg.norm(diff, axis=-1)
    d_safe = np.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    # Smoothed denominator 1/(d² + ε²): bounded at d=0, converges to 1/d² far
    # away, and C∞ everywhere — no kink at the soft-core boundary.
    mag = 1.0 / (d_safe * d_safe + soft_core_radius * soft_core_radius)
    np.fill_diagonal(mag, 0.0)

    mass_pair = weights[:, None] * weights[None, :]
    forces = (k_r * mag * mass_pair)[..., None] * direction  # (N, N, D)
    return forces.sum(axis=1)


def _pairwise_repulsion_sparse(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    cutoff: float,
) -> np.ndarray:
    """Sparse repulsion: only compute forces for pairs within `cutoff` distance.

    Uses scipy cKDTree.query_pairs to enumerate nearby pairs without building
    the full N×N distance matrix. Scatter accumulation via np.bincount avoids
    the slow np.add.at unbuffered loop.
    """
    from scipy.spatial import cKDTree

    n, d = positions.shape
    tree = cKDTree(positions)
    try:
        pairs = tree.query_pairs(cutoff, output_type="ndarray")
    except TypeError:
        raw = tree.query_pairs(cutoff)
        pairs = np.array(list(raw), dtype=np.int64) if raw else np.zeros((0, 2), dtype=np.int64)

    forces = np.zeros_like(positions)
    if pairs.shape[0] == 0:
        return forces

    i_idx, j_idx = pairs[:, 0], pairs[:, 1]
    diff = positions[i_idx] - positions[j_idx]
    d_sq = np.einsum("ij,ij->i", diff, diff)
    d_safe = np.sqrt(np.maximum(d_sq, 1e-12))
    direction = diff / d_safe[:, None]
    mag = 1.0 / (d_sq + soft_core_radius * soft_core_radius)
    mass_pair = weights[i_idx] * weights[j_idx]
    f = (k_r * mag * mass_pair)[:, None] * direction  # (P, D)

    # np.bincount scatter — vectorised per dimension, much faster than add.at
    for dim in range(d):
        forces[:, dim] += np.bincount(i_idx, weights=f[:, dim], minlength=n)
        forces[:, dim] -= np.bincount(j_idx, weights=f[:, dim], minlength=n)
    return forces


def pairwise_attraction(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
) -> np.ndarray:
    n = positions.shape[0]
    if n < 2:
        return np.zeros_like(positions)

    diff = positions[None, :, :] - positions[:, None, :]  # j - i, toward j
    d = np.linalg.norm(diff, axis=-1)
    d_safe = np.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    # Soft core flattens magnitude inside the core radius so close pairs do not
    # gain unbounded pull and fight the repulsion forever.
    flat_mag = 1.0 / (soft_core_radius * soft_core_radius)
    inv_sq = 1.0 / (d_safe * d_safe)
    near = d < soft_core_radius
    mag = np.where(near, flat_mag, inv_sq)
    np.fill_diagonal(mag, 0.0)

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
    """Hooke's Law spring along explicit edges with a defined rest length.

    F = k_e * (d - L₀). Attractive when d > L₀, repulsive when d < L₀, zero
    at d == L₀. Equilibrium is geometrically fixed rather than emergent.
    """
    forces = np.zeros_like(positions)
    if edges.shape[0] == 0:
        return forces
    i_idx = edges[:, 0]
    j_idx = edges[:, 1]
    diff = positions[j_idx] - positions[i_idx]
    d = np.linalg.norm(diff, axis=-1)
    d_safe = np.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[:, None]
    f = (k_e * (d - rest_length))[:, None] * direction
    np.add.at(forces, i_idx, f)
    np.add.at(forces, j_idx, -f)
    return forces
