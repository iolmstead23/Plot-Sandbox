"""Enqueue an add_node mutation for a random new node."""

import numpy as np

from packages.config import config

from . import mutate


_rng = np.random.default_rng()


def add_random_node(app) -> None:
    sim = config.simulation
    weight = float(_rng.uniform(sim.weight_min, sim.weight_max))
    direction = _rng.normal(size=3)
    direction /= np.linalg.norm(direction) + 1e-12
    position = direction * sim.spawn_distance
    mutate.queue_add_node(weight, position)
