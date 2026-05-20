"""CUDA C source for the fused N-body step kernel.

Kept in its own module so _forces_gpu_fused.py stays under the line limit
and the kernel text is easy to diff in isolation.
"""

_REPULSION_STANDARD = """\
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
"""

_REPULSION_LINLOG = """\
    for (int j = 0; j < N; ++j) {
        if (j == i) continue;
        float dr0 = pi0 - pos[j*3+0];
        float dr1 = pi1 - pos[j*3+1];
        float dr2 = pi2 - pos[j*3+2];
        float d2   = dr0*dr0 + dr1*dr1 + dr2*dr2;
        if (cutoff2 > 0.0f && d2 > cutoff2) continue;
        float mag  = k_r * weights[j] / sqrtf(d2 + sc2);
        float invd = rsqrtf(d2 + 1e-9f);
        f0 += mag * dr0 * invd;
        f1 += mag * dr1 * invd;
        f2 += mag * dr2 * invd;
    }
"""


def make_kernel_src(linlog: bool = False) -> str:
    """Return the kernel source with the requested repulsion formula."""
    repulsion = _REPULSION_LINLOG if linlog else _REPULSION_STANDARD
    return _KERNEL_SRC.replace(_REPULSION_STANDARD, repulsion)


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
       Pairwise repulsion — all N-1 neighbours (standard mode)
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
