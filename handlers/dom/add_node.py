import numpy as np

from packages.config import config
from packages.dom import dom

from . import mutate

_rng = np.random.default_rng()


def add_random_node(app) -> None:
    sim = config.simulation
    weight = float(_rng.uniform(sim.weight_min, sim.weight_max))
    direction = _rng.normal(size=sim.dims)
    direction /= np.linalg.norm(direction) + 1e-12
    position = direction * sim.spawn_distance

    def _action() -> None:
        existing_n = dom.n
        dom.add_node(weight, position)
        if existing_n > 0:
            target = int(_rng.integers(0, existing_n))
            dom.add_edge(dom.n - 1, target)

    mutate.queue(_action)
