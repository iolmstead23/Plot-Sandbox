"""Barnes-Hut O(N log N) repulsion via Numba-JIT octree — CPU only.

Activated from forces.py when N >= BH_THRESHOLD, Numba is available, and
the CPU path is active.  The GPU chunked path handles GPU workloads.

Algorithm
---------
Phase 1 — build: insert all N particles into a flat-array octree.
Phase 2 — COM:   bottom-up pass computes centre-of-mass per node.
Phase 3 — force: parallel DFS traversal; far nodes collapsed to one mass
          when (node_size / distance) < theta (opening criterion).

With Numba `prange`, force computation parallelises across all CPU cores.
"""

from __future__ import annotations

import numpy as np

BH_THRESHOLD: int = 5000   # activate when N >= this on CPU path
BH_THETA: float   = 0.7    # opening criterion — larger is faster, less exact
_MAX_NODES_FACTOR = 8      # pre-allocate 8 * N octree nodes
_MAX_DEPTH        = 64     # recursion guard
_MAX_STACK        = 1024   # DFS stack depth per particle

_numba_ok: bool | None = None
_jit_fn = None             # set on first call to repulsion()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def available() -> bool:
    """True when Numba is installed and Barnes-Hut can run."""
    global _numba_ok
    if _numba_ok is None:
        try:
            import numba  # noqa: F401
            _numba_ok = True
        except ImportError:
            _numba_ok = False
    return _numba_ok


def repulsion(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
    theta: float = BH_THETA,
) -> np.ndarray:
    """Return (N, 3) repulsive forces, O(N log N).  Requires Numba and D=3."""
    if not available():
        raise RuntimeError("Barnes-Hut requires Numba: pip install numba")
    if positions.shape[1] != 3:
        raise ValueError(f"Barnes-Hut requires D=3, got D={positions.shape[1]}")

    _ensure_compiled()
    assert _jit_fn is not None
    pos64 = np.ascontiguousarray(positions, dtype=np.float64)
    w64   = np.ascontiguousarray(weights,   dtype=np.float64)
    forces = _jit_fn(pos64, w64, float(k_r), float(soft_core_radius), float(theta))
    return forces.astype(positions.dtype)


# ---------------------------------------------------------------------------
# Lazy JIT compilation
# ---------------------------------------------------------------------------

def _ensure_compiled() -> None:
    global _jit_fn
    if _jit_fn is not None:
        return

    import numba as nb

    # ---- Helpers -----------------------------------------------------------

    @nb.njit(cache=True)
    def _oct_index(pos_i, cx, cy, cz):
        return ((1 if pos_i[0] >= cx else 0) |
                (2 if pos_i[1] >= cy else 0) |
                (4 if pos_i[2] >= cz else 0))

    @nb.njit(cache=True)
    def _init_node(k, bmin_k, bmax_k, bmin, bmax, pcount, leaf_idx, children):
        bmin[k, 0] = bmin_k[0]; bmin[k, 1] = bmin_k[1]; bmin[k, 2] = bmin_k[2]
        bmax[k, 0] = bmax_k[0]; bmax[k, 1] = bmax_k[1]; bmax[k, 2] = bmax_k[2]
        pcount[k]   = 0
        leaf_idx[k] = -1
        for c in range(8):
            children[k, c] = -1

    @nb.njit(cache=True)
    def _child_bounds(parent, oct, bmin, bmax, cmin_out, cmax_out):
        cx = (bmin[parent, 0] + bmax[parent, 0]) * 0.5
        cy = (bmin[parent, 1] + bmax[parent, 1]) * 0.5
        cz = (bmin[parent, 2] + bmax[parent, 2]) * 0.5
        cmin_out[0] = cx if (oct & 1) else bmin[parent, 0]
        cmax_out[0] = bmax[parent, 0] if (oct & 1) else cx
        cmin_out[1] = cy if (oct & 2) else bmin[parent, 1]
        cmax_out[1] = bmax[parent, 1] if (oct & 2) else cy
        cmin_out[2] = cz if (oct & 4) else bmin[parent, 2]
        cmax_out[2] = bmax[parent, 2] if (oct & 4) else cz

    # ---- Phase 1: Tree construction ----------------------------------------

    @nb.njit(cache=True)
    def _insert(pid, pos, node, depth,
                bmin, bmax, pcount, leaf_idx, children, n_used, max_nodes):
        """Insert particle pid into subtree rooted at node (structure only)."""
        if depth > _MAX_DEPTH or n_used[0] >= max_nodes:
            return

        if pcount[node] == 0:
            leaf_idx[node] = pid
            pcount[node]   = 1
            return

        cx = (bmin[node, 0] + bmax[node, 0]) * 0.5
        cy = (bmin[node, 1] + bmax[node, 1]) * 0.5
        cz = (bmin[node, 2] + bmax[node, 2]) * 0.5

        if pcount[node] == 1:
            # Occupied leaf — split: push existing particle into a child first.
            old_pid = leaf_idx[node]
            leaf_idx[node] = -1
            pcount[node]   = 2

            oct_old = _oct_index(pos[old_pid], cx, cy, cz)
            if children[node, oct_old] == -1:
                k = n_used[0]; n_used[0] += 1
                cmin = np.empty(3); cmax = np.empty(3)
                _child_bounds(node, oct_old, bmin, bmax, cmin, cmax)
                _init_node(k, cmin, cmax, bmin, bmax, pcount, leaf_idx, children)
                children[node, oct_old] = k
            _insert(old_pid, pos, children[node, oct_old], depth + 1,
                    bmin, bmax, pcount, leaf_idx, children, n_used, max_nodes)
        else:
            pcount[node] += 1

        oct_new = _oct_index(pos[pid], cx, cy, cz)
        if children[node, oct_new] == -1:
            k = n_used[0]; n_used[0] += 1
            cmin = np.empty(3); cmax = np.empty(3)
            _child_bounds(node, oct_new, bmin, bmax, cmin, cmax)
            _init_node(k, cmin, cmax, bmin, bmax, pcount, leaf_idx, children)
            children[node, oct_new] = k
        _insert(pid, pos, children[node, oct_new], depth + 1,
                bmin, bmax, pcount, leaf_idx, children, n_used, max_nodes)

    # ---- Phase 2: Centre-of-mass (bottom-up) --------------------------------

    @nb.njit(cache=True)
    def _compute_com(node, pos, weights, pcount, leaf_idx, children, com, mass):
        if pcount[node] == 0:
            mass[node] = 0.0
            return
        if pcount[node] == 1:
            p = leaf_idx[node]
            mass[node]   = weights[p]
            com[node, 0] = pos[p, 0]
            com[node, 1] = pos[p, 1]
            com[node, 2] = pos[p, 2]
            return
        # Internal: aggregate children.
        m_total = 0.0
        wx = wy = wz = 0.0
        for c in range(8):
            child = children[node, c]
            if child == -1:
                continue
            _compute_com(child, pos, weights, pcount, leaf_idx, children, com, mass)
            m_c = mass[child]
            m_total += m_c
            wx += com[child, 0] * m_c
            wy += com[child, 1] * m_c
            wz += com[child, 2] * m_c
        mass[node] = m_total
        if m_total > 0.0:
            com[node, 0] = wx / m_total
            com[node, 1] = wy / m_total
            com[node, 2] = wz / m_total

    # ---- Phase 3: Force computation (parallel) ------------------------------

    @nb.njit(cache=True)
    def _force_on(pi, pos, weights, k_r, sc2, theta2,
                  bmin, bmax, com, mass, pcount, leaf_idx, children):
        """DFS traversal: repulsive force on particle pi."""
        fx = fy = fz = 0.0
        stack = np.empty(_MAX_STACK, dtype=np.int32)
        stack[0] = 0   # push root
        sp = 1

        while sp > 0:
            sp -= 1
            node = stack[sp]

            if pcount[node] == 0:
                continue

            # Distance from pi to this node's COM.
            dx = pos[pi, 0] - com[node, 0]
            dy = pos[pi, 1] - com[node, 1]
            dz = pos[pi, 2] - com[node, 2]
            d2 = dx * dx + dy * dy + dz * dz

            if pcount[node] == 1:
                # Leaf — exact force, skip self.
                if leaf_idx[node] == pi:
                    continue
                if d2 > 0.0:
                    mag = k_r * weights[pi] * mass[node] / (d2 + sc2)
                    inv_d = 1.0 / (d2 ** 0.5)
                    fx += mag * dx * inv_d
                    fy += mag * dy * inv_d
                    fz += mag * dz * inv_d
                continue

            # Internal node: check Barnes-Hut opening criterion.
            # node_size = max side length of bounding box.
            sx = bmax[node, 0] - bmin[node, 0]
            sy = bmax[node, 1] - bmin[node, 1]
            sz = bmax[node, 2] - bmin[node, 2]
            s2 = max(sx, max(sy, sz)) ** 2

            if d2 > 0.0 and s2 < theta2 * d2:
                # Far enough: treat entire node as one mass at COM.
                mag = k_r * weights[pi] * mass[node] / (d2 + sc2)
                inv_d = 1.0 / (d2 ** 0.5)
                fx += mag * dx * inv_d
                fy += mag * dy * inv_d
                fz += mag * dz * inv_d
            else:
                # Too close: descend into children.
                for c in range(8):
                    child = children[node, c]
                    if child != -1 and sp < _MAX_STACK:
                        stack[sp] = child
                        sp += 1

        return fx, fy, fz

    @nb.njit(cache=True, parallel=True)
    def _compute_forces_impl(pos, weights, k_r, sc2, theta2,
                              bmin, bmax, com, mass, pcount, leaf_idx, children):
        n = pos.shape[0]
        forces = np.zeros((n, 3), dtype=np.float64)
        for pi in nb.prange(n):
            fx, fy, fz = _force_on(pi, pos, weights, k_r, sc2, theta2,
                                    bmin, bmax, com, mass, pcount, leaf_idx, children)
            forces[pi, 0] = fx
            forces[pi, 1] = fy
            forces[pi, 2] = fz
        return forces

    # ---- Top-level wrapper -------------------------------------------------

    @nb.njit(cache=True)
    def _run(pos, weights, k_r, soft_core_radius, theta):
        n = pos.shape[0]
        max_nodes = max(n * _MAX_NODES_FACTOR, 64)
        sc2    = soft_core_radius * soft_core_radius
        theta2 = theta * theta

        # Pre-allocate tree arrays.
        bmin     = np.empty((max_nodes, 3), dtype=np.float64)
        bmax     = np.empty((max_nodes, 3), dtype=np.float64)
        com      = np.zeros((max_nodes, 3), dtype=np.float64)
        mass     = np.zeros(max_nodes,      dtype=np.float64)
        pcount   = np.zeros(max_nodes,      dtype=np.int32)
        leaf_idx = np.full(max_nodes, -1,   dtype=np.int32)
        children = np.full((max_nodes, 8), -1, dtype=np.int32)
        n_used   = np.zeros(1, dtype=np.int32)

        # Root node spans a padded bounding box.
        lo = np.empty(3); hi = np.empty(3)
        for d in range(3):
            lo[d] = pos[:, d].min() - 1e-4
            hi[d] = pos[:, d].max() + 1e-4
        n_used[0] = 1
        _init_node(0, lo, hi, bmin, bmax, pcount, leaf_idx, children)

        # Phase 1: insert all particles.
        for i in range(n):
            _insert(i, pos, 0, 0, bmin, bmax, pcount, leaf_idx, children, n_used, max_nodes)

        # Phase 2: bottom-up COM.
        _compute_com(0, pos, weights, pcount, leaf_idx, children, com, mass)

        # Phase 3: parallel force computation.
        return _compute_forces_impl(pos, weights, k_r, sc2, theta2,
                                     bmin, bmax, com, mass, pcount, leaf_idx, children)

    _jit_fn = _run
