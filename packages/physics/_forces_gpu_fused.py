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

# ---------------------------------------------------------------------------
# CUDA kernel source
# ---------------------------------------------------------------------------

_KERNEL_SRC = r"""
extern "C" __global__ void nbody_fused_step(
    const float* __restrict__ pos,            /* (N, 3)  input positions  */
    float* __restrict__       new_pos,        /* (N, 3)  output positions */
    const float* __restrict__ weights,        /* (N,)                     */
    const unsigned char* __restrict__ pinned, /* (N,)  0=free, 1=pinned   */
    const int* __restrict__   edges,          /* (2*E,) flat [a0,b0,...]  */
    int N, int E,
    float k_g, float k_r, float k_e,
    float edge_rest_len, float sc_radius,
    float F_max, float max_step,
    float dt, float temperature,
    float fx, float fy, float fz,             /* gravity focus point      */
    float cutoff2                             /* squared repulsion cutoff; 0=unlimited */
)
{
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= N) return;

    const float sc2 = sc_radius * sc_radius;
    const float pi0 = pos[i*3+0];
    const float pi1 = pos[i*3+1];
    const float pi2 = pos[i*3+2];
    const float wi  = weights[i];

    /* ------------------------------------------------------------------
       Central gravity
       F = -k_g * w * (pos - focus) / r_soft
       r_soft = sqrt(|pos - focus|^2 + sc^2)
       ------------------------------------------------------------------ */
    float dg0 = pi0 - fx, dg1 = pi1 - fy, dg2 = pi2 - fz;
    float r_soft = sqrtf(dg0*dg0 + dg1*dg1 + dg2*dg2 + sc2);
    float gscale = -k_g * wi / r_soft;
    float f0 = gscale * dg0;
    float f1 = gscale * dg1;
    float f2 = gscale * dg2;

    /* ------------------------------------------------------------------
       Pairwise repulsion — all N-1 neighbours
       F_i += k_r * w_i * w_j / (d^2 + sc^2) * (pos_i - pos_j) / |d|
       ------------------------------------------------------------------ */
    for (int j = 0; j < N; ++j) {
        if (j == i) continue;
        float dr0 = pi0 - pos[j*3+0];
        float dr1 = pi1 - pos[j*3+1];
        float dr2 = pi2 - pos[j*3+2];
        float d2   = dr0*dr0 + dr1*dr1 + dr2*dr2;
        if (cutoff2 > 0.0f && d2 > cutoff2) continue;
        float mag  = k_r * wi * weights[j] / (d2 + sc2);
        float invd = rsqrtf(d2 + 1e-9f);
        f0 += mag * dr0 * invd;
        f1 += mag * dr1 * invd;
        f2 += mag * dr2 * invd;
    }

    /* ------------------------------------------------------------------
       Edge spring forces — Hooke's Law
       F_i += k_e * (dist - L0) * (pos_j - pos_i) / dist
       Symmetric: same formula whether i is the first or second endpoint.
       ------------------------------------------------------------------ */
    for (int e = 0; e < E; ++e) {
        int a = edges[2*e], b = edges[2*e + 1];
        int j = (a == i) ? b : (b == i) ? a : -1;
        if (j < 0) continue;
        float de0 = pos[j*3+0] - pi0;
        float de1 = pos[j*3+1] - pi1;
        float de2 = pos[j*3+2] - pi2;
        float dist   = sqrtf(de0*de0 + de1*de1 + de2*de2 + 1e-9f);
        float escale = k_e * (dist - edge_rest_len) / dist;
        f0 += escale * de0;
        f1 += escale * de1;
        f2 += escale * de2;
    }

    /* ------------------------------------------------------------------
       Force magnitude cap — preserves direction, bounds blow-ups
       ------------------------------------------------------------------ */
    float fnorm = sqrtf(f0*f0 + f1*f1 + f2*f2);
    if (fnorm > F_max) {
        float inv = F_max / fnorm;
        f0 *= inv; f1 *= inv; f2 *= inv;
    }

    /* ------------------------------------------------------------------
       Pinned nodes: hold position, skip integration
       ------------------------------------------------------------------ */
    if (pinned[i]) {
        new_pos[i*3+0] = pi0;
        new_pos[i*3+1] = pi1;
        new_pos[i*3+2] = pi2;
        return;
    }

    /* ------------------------------------------------------------------
       Integration step + step magnitude cap
       ------------------------------------------------------------------ */
    float s0 = f0 * dt * temperature;
    float s1 = f1 * dt * temperature;
    float s2 = f2 * dt * temperature;
    float snorm = sqrtf(s0*s0 + s1*s1 + s2*s2);
    if (snorm > max_step) {
        float inv = max_step / snorm;
        s0 *= inv; s1 *= inv; s2 *= inv;
    }

    new_pos[i*3+0] = pi0 + s0;
    new_pos[i*3+1] = pi1 + s1;
    new_pos[i*3+2] = pi2 + s2;
}
"""

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
