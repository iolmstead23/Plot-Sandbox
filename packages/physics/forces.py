"""Pure force functions — array-backend-agnostic via _backend.get_module().

Each function resolves its array module (numpy or cupy) from the positions
argument so the same code runs on CPU or GPU without modification.

No imports from other packages. DOM is never referenced here.
"""

import numpy as np

from ._backend import get_module, is_gpu


# ---------------------------------------------------------------------------
# scipy availability check (CPU path only)
# ---------------------------------------------------------------------------

_scipy_ok: bool | None = None

# Maximum bytes for the (chunk, N, D) diff intermediate array.
# Keeping each diff under 1 GB means 6–8 live intermediates peak at ~6 GB,
# comfortably within 16 GB VRAM.  For N ≤ ~18 000 the chunk equals N, so
# the GPU loop runs exactly once — same as the original dense path.
_DIFF_BYTES_MAX: int = 1 * 1024 ** 3  # 1 GB


def _gpu_chunk_for(n: int, d: int, itemsize: int) -> int:
    """Row count so (chunk, N, D) diff stays under _DIFF_BYTES_MAX."""
    per_row = n * d * itemsize
    return max(min(n, _DIFF_BYTES_MAX // per_row), 64)


def _scipy_available() -> bool:
    global _scipy_ok
    if _scipy_ok is None:
        try:
            import scipy.spatial  # noqa: F401
            _scipy_ok = True
        except ImportError:
            _scipy_ok = False
    return _scipy_ok


# ---------------------------------------------------------------------------
# Forces
# ---------------------------------------------------------------------------


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

    # GPU: chunked path caps peak VRAM at O(_CHUNK·N·D) instead of O(N²·D).
    if xp is not np:
        return _pairwise_repulsion_chunked_gpu(
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
    if cutoff > 0.0 and n >= 150 and _scipy_available():
        return _pairwise_repulsion_sparse(
            positions, weights, k_r=k_r,
            soft_core_radius=soft_core_radius, cutoff=cutoff,
        )

    # CPU dense fallback — builds (N, N, D) intermediary.
    diff = positions[:, None, :] - positions[None, :, :]  # (N, N, D)
    d = xp.linalg.norm(diff, axis=-1)
    d_safe = xp.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    # Smoothed 1/(d² + ε²): bounded at d=0, C∞ everywhere.
    mag = 1.0 / (d_safe * d_safe + soft_core_radius * soft_core_radius)
    xp.fill_diagonal(mag, 0.0)

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
    """Sparse repulsion (CPU only): O(N log N + P) via scipy cKDTree."""
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

    for dim in range(d):
        forces[:, dim] += np.bincount(i_idx, weights=f[:, dim], minlength=n)
        forces[:, dim] -= np.bincount(j_idx, weights=f[:, dim], minlength=n)
    return forces


def _pairwise_repulsion_chunked_gpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
) -> np.ndarray:
    """GPU repulsion: row-chunked to cap peak VRAM at O(_CHUNK·N·D).

    Processes the N×N pair matrix in blocks of _CHUNK rows so each iteration
    allocates (_CHUNK, N, D) instead of (N, N, D) — identical physics to the
    original dense path, just bounded memory.  No cutoff is applied here; the
    GPU path always computes exact all-pairs forces.
    """
    xp = get_module(positions)
    n, d = positions.shape
    forces = xp.zeros_like(positions)
    dtype = positions.dtype
    zero  = dtype.type(0.0)
    one   = dtype.type(1.0)
    sc2   = dtype.type(soft_core_radius * soft_core_radius)
    chunk = _gpu_chunk_for(n, d, dtype.itemsize)

    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        b = end - start

        diff = positions[start:end, None, :] - positions[None, :, :]  # (B, N, D)
        d2 = (diff * diff).sum(axis=-1)                                # (B, N)

        d_safe = xp.where(d2 > zero, xp.sqrt(d2), one)
        direction = diff / d_safe[..., None]
        mag = one / (d2 + sc2)

        # Zero self-interaction using GPU-side arithmetic (avoids HtoD transfer).
        local_rows  = xp.arange(b, dtype=xp.int64)
        global_cols = local_rows + start
        mag[local_rows, global_cols] = zero

        mass_pair = weights[start:end, None] * weights[None, :]  # (B, N)
        forces[start:end] = ((k_r * mag * mass_pair)[..., None] * direction).sum(axis=1)

    return forces


def _pairwise_attraction_chunked_gpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
) -> np.ndarray:
    """GPU attraction: row-chunked to bound peak VRAM at O(_CHUNK·N·D).

    Identical physics to the original dense all-pairs path; no cutoff applied.
    """
    xp = get_module(positions)
    n, d = positions.shape
    forces = xp.zeros_like(positions)
    dtype = positions.dtype
    zero     = dtype.type(0.0)
    one      = dtype.type(1.0)
    flat_mag = dtype.type(1.0 / (soft_core_radius * soft_core_radius))
    sc_thresh = dtype.type(soft_core_radius)
    chunk = _gpu_chunk_for(n, d, dtype.itemsize)

    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        b = end - start

        # diff[b, j] = pos[j] - pos[start+b] — pointing toward j (attraction).
        diff = positions[None, :, :] - positions[start:end, None, :]  # (B, N, D)
        d2 = (diff * diff).sum(axis=-1)                                # (B, N)
        d_safe = xp.where(d2 > zero, xp.sqrt(d2), one)
        direction = diff / d_safe[..., None]

        inv_sq = one / (d_safe * d_safe)
        mag = xp.where(d_safe < sc_thresh, flat_mag, inv_sq)

        local_rows  = xp.arange(b, dtype=xp.int64)
        global_cols = local_rows + start
        mag[local_rows, global_cols] = zero

        mass_pair = weights[start:end, None] * weights[None, :]
        forces[start:end] = ((k_a * mag * mass_pair)[..., None] * direction).sum(axis=1)

    return forces


def _pairwise_attraction_sparse_cpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
    cutoff: float,
) -> np.ndarray:
    """CPU sparse attraction: O(N log N + P·D) via scipy cKDTree."""
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
        return _pairwise_attraction_chunked_gpu(
            positions, weights, k_a=k_a,
            soft_core_radius=soft_core_radius,
        )

    if cutoff > 0.0 and n >= 150 and _scipy_available():
        return _pairwise_attraction_sparse_cpu(
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

    F = k_e * (d - L₀). Attractive when d > L₀, repulsive when d < L₀.
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
