import numpy as np

from packages.config import config


def build() -> dict:
    p = config.physics
    dims = config.simulation.dims
    focus = np.zeros(dims, dtype=np.float64)
    focus[: min(3, dims)] = np.asarray(p.focus, dtype=np.float64)[: min(3, dims)]
    return {
        "k_central": p.k_central,
        "k_repel": p.k_repel,
        "k_attract": p.k_attract,
        "k_edge": p.k_edge,
        "edge_rest_length": p.edge_rest_length,
        "soft_core_radius": p.soft_core_radius,
        "max_step": p.max_step,
        "F_max": p.F_max,
        "focus": focus,
        "repulsion_cutoff": p.repulsion_cutoff,
    }
