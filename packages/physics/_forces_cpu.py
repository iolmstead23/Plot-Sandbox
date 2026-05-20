"""CPU-specific force kernels — sparse paths via scipy cKDTree."""

import numpy as np

_scipy_ok: bool | None = None


def scipy_available() -> bool:
    global _scipy_ok
    if _scipy_ok is None:
        try:
            import scipy.spatial  # noqa: F401
            _scipy_ok = True
        except ImportError:
            _scipy_ok = False
    return _scipy_ok


def pairwise_repulsion_sparse(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    cutoff: float,
    linlog: bool = False,
) -> np.ndarray:
    """Sparse repulsion (CPU only): O(N log N + P) via scipy cKDTree."""
    from scipy.spatial import cKDTree  # type: ignore[attr-defined]

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

    if linlog:
        sc2 = soft_core_radius * soft_core_radius
        d_lin = np.sqrt(d_sq + sc2)
        mag = 1.0 / d_lin
        # Force on i from j uses w_j (radiating weight); force on j from i uses w_i.
        f_i = (k_r * mag * weights[j_idx])[:, None] * direction
        f_j = (k_r * mag * weights[i_idx])[:, None] * (-direction)
        for dim in range(d):
            forces[:, dim] += np.bincount(i_idx, weights=f_i[:, dim], minlength=n)
            forces[:, dim] += np.bincount(j_idx, weights=f_j[:, dim], minlength=n)
    else:
        mag = 1.0 / (d_sq + soft_core_radius * soft_core_radius)
        mass_pair = weights[i_idx] * weights[j_idx]
        f = (k_r * mag * mass_pair)[:, None] * direction
        for dim in range(d):
            forces[:, dim] += np.bincount(i_idx, weights=f[:, dim], minlength=n)
            forces[:, dim] -= np.bincount(j_idx, weights=f[:, dim], minlength=n)

    return forces


def pairwise_attraction_sparse_cpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
    cutoff: float,
) -> np.ndarray:
    """CPU sparse attraction: O(N log N + P*D) via scipy cKDTree."""
    from scipy.spatial import cKDTree  # type: ignore[attr-defined]

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
    diff    = positions[j_idx] - positions[i_idx]        # toward j
    d_sq    = np.einsum("ij,ij->i", diff, diff)
    d_safe  = np.sqrt(np.maximum(d_sq, 1e-12))
    direction = diff / d_safe[:, None]

    flat_mag = 1.0 / (soft_core_radius * soft_core_radius)
    inv_sq   = 1.0 / (d_safe * d_safe)
    mag = np.where(d_safe < soft_core_radius, flat_mag, inv_sq)

    mass_pair = weights[i_idx] * weights[j_idx]
    f = (k_a * mag * mass_pair)[:, None] * direction     # (P, D)

    np.add.at(forces, i_idx,  f)
    np.add.at(forces, j_idx, -f)
    return forces
