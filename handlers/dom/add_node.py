import numpy as np

from packages.config import config
from packages.dom import dom

from . import mutate
from .weights import recompute_weights_from_degree

_rng = np.random.default_rng()


def add_random_node(_app) -> None:
    sim = config.simulation
    direction = _rng.normal(size=sim.dims)
    direction /= np.linalg.norm(direction) + 1e-12
    position = direction * sim.spawn_distance

    def _action() -> None:
        existing_n = dom.n
        dom.add_node(1.0, position)
        if existing_n > 0:
            target = int(_rng.integers(0, existing_n))
            dom.add_edge(dom.n - 1, target)
        recompute_weights_from_degree()

    mutate.queue(_action)
