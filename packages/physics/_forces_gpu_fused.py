"""Single-launch fused N-body step kernel for 3-D GPU simulations.

For N up to ~18 000 the full position array (N*3*4 bytes) fits in GPU L1
cache, so a naive O(N²) kernel runs entirely from register/L1 traffic.
Replacing the ~40 separate CuPy elementwise kernels per relax_step with one
CUDA launch removes the dominant Python/CuPy dispatch overhead — the actual
GPU arithmetic for N=750 takes nanoseconds, while each CuPy call costs
~10-50 μs of Python overhead.

Exported surface
----------------
relax_step_fused_gpu  — drop-in replacement for the multi-kernel chain in
                        integrator.py when positions are already on GPU and
                        D == 3 with a non-empty edge list.
"""

import numpy as np

from ._backend import get_module
from ._kernel_src import _KERNEL_SRC

# ---------------------------------------------------------------------------
# Kernel handle — compiled once on first call, then reused
# ---------------------------------------------------------------------------

_kernel = None
_BLOCK = 128


def _get_kernel():
    global _kernel
    if _kernel is None:
        import cupy as cp
        _kernel = cp.RawKernel(_KERNEL_SRC, "nbody_fused_step")
    return _kernel


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def relax_step_fused_gpu(
    positions,
    weights,
    pinned,
    *,
    edges,
    dt: float,
    temperature: float,
    params: dict,
):
    """One CUDA kernel launch replacing the ~40-kernel CuPy chain.

    All array inputs must already be CuPy arrays (positions/weights float32,
    pinned uint8, edges int32).  Returns a new float32 CuPy array (N, 3).

    Only called when D == 3 and the edge list is non-empty; the integrator
    falls back to the multi-kernel path for any other configuration.
    """
    import cupy as cp

    xp = get_module(positions)
    N = positions.shape[0]
    p = params

    pos32  = positions.astype(cp.float32, copy=False)
    w32    = weights.astype(cp.float32, copy=False)
    pin_u8 = xp.asarray(pinned, dtype=cp.uint8)

    if edges is not None and edges.shape[0] > 0:
        edges_i32 = xp.asarray(edges, dtype=cp.int32).ravel()
        E = int(edges.shape[0])
    else:
        edges_i32 = xp.empty(0, dtype=cp.int32)
        E = 0

    new_pos = xp.empty_like(pos32)

    focus   = p["focus"]
    cutoff  = float(p.get("repulsion_cutoff", 0.0))
    grid    = (int(np.ceil(N / _BLOCK)),)
    block   = (_BLOCK,)

    _get_kernel()(
        grid, block,
        (
            pos32, new_pos, w32, pin_u8, edges_i32,
            np.int32(N),  np.int32(E),
            np.float32(p["k_central"]),
            np.float32(p["k_repel"]),
            np.float32(p["k_edge"]),
            np.float32(p["edge_rest_length"]),
            np.float32(p["soft_core_radius"]),
            np.float32(p["F_max"]),
            np.float32(p["max_step"]),
            np.float32(dt),
            np.float32(temperature),
            np.float32(float(focus[0]) if len(focus) > 0 else 0.0),
            np.float32(float(focus[1]) if len(focus) > 1 else 0.0),
            np.float32(float(focus[2]) if len(focus) > 2 else 0.0),
            np.float32(cutoff * cutoff),
        ),
    )

    return new_pos
