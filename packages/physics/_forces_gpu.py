"""GPU-specific force kernels — row-chunked to bound peak VRAM usage."""

import numpy as np

from ._backend import get_module

# Maximum bytes for the (chunk, N, D) diff intermediate array.
# Keeping each diff under 1 GB means 6-8 live intermediates peak at ~6 GB,
# comfortably within 16 GB VRAM.  For N <= ~18 000 the chunk equals N, so
# the GPU loop runs exactly once — same as the original dense path.
_DIFF_BYTES_MAX: int = 1 * 1024 ** 3  # 1 GB


def _gpu_chunk_for(n: int, d: int, itemsize: int) -> int:
    """Row count so (chunk, N, D) diff stays under _DIFF_BYTES_MAX."""
    per_row = n * d * itemsize
    return max(min(n, _DIFF_BYTES_MAX // per_row), 64)


def pairwise_repulsion_chunked_gpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
) -> np.ndarray:
    """GPU repulsion: row-chunked to cap peak VRAM at O(_CHUNK*N*D).

    Processes the N*N pair matrix in blocks of _CHUNK rows so each iteration
    allocates (_CHUNK, N, D) instead of (N, N, D) — identical physics to the
    original dense path, just bounded memory.  No cutoff applied here; the
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


def pairwise_attraction_chunked_gpu(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
) -> np.ndarray:
    """GPU attraction: row-chunked to bound peak VRAM at O(_CHUNK*N*D).

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
