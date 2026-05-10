import numpy as np

from packages.config import config

_focus = np.zeros(config.simulation.dims, dtype=np.float64)
_focus[: min(3, config.simulation.dims)] = np.asarray(
    config.physics.focus, dtype=np.float64
)[: min(3, config.simulation.dims)]


def build() -> dict:
    p = config.physics
    return {
        "k_central": p.k_central,
        "k_repel": p.k_repel,
        "k_attract": p.k_attract,
        "k_edge": p.k_edge,
        "edge_rest_length": p.edge_rest_length,
        "soft_core_radius": p.soft_core_radius,
        "max_step": p.max_step,
        "F_max": p.F_max,
        "focus": _focus,
    }
