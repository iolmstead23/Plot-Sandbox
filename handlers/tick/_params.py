import numpy as np

from packages.config import config
from packages.dom import dom


def build() -> dict:
    p = config.physics
    dims = config.simulation.dims
    focus = np.zeros(dims, dtype=np.float64)
    focus[: min(3, dims)] = np.asarray(p.focus, dtype=np.float64)[: min(3, dims)]

    # Both force constants are stored as per-node ratios in config.
    # Multiplying by N gives the actual strength used by the integrator,
    # keeping the gravity/repulsion balance identical at any node count.
    n = max(1, dom.n)

    return {
        "k_central": p.gravity_ratio * n,
        "k_repel": p.repel_ratio * n,
        "k_attract": p.k_attract / n,
        "k_edge": p.k_edge,
        "edge_rest_length": p.edge_rest_length,
        "soft_core_radius": p.soft_core_radius,
        "max_step": p.max_step,
        "F_max": p.F_max,
        "focus": focus,
        "repulsion_cutoff": p.repulsion_cutoff,
        "bh_threshold": p.bh_threshold,
        "bh_theta": p.bh_theta,
        "cpu_sparse_threshold": p.cpu_sparse_threshold,
        "linlog_repulsion": p.linlog_repulsion,
    }
