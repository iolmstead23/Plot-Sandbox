import numpy as np

from packages.config import config
from packages.dom import dom

from . import mutate
from .weights import recompute_weights_from_degree
from ..state import node_temperature, temperature

_rng = np.random.default_rng()


def add_random_node(_app) -> None:
    sim = config.simulation
    direction = _rng.normal(size=sim.dims)
    direction /= np.linalg.norm(direction) + 1e-12
    position = direction * sim.spawn_distance

    def _action() -> None:
        existing_n = dom.n
        dom.add_node(1.0, position)
        neighbor: int | None = None
        if existing_n > 0:
            neighbor = int(_rng.integers(0, existing_n))
            dom.add_edge(dom.n - 1, neighbor)
        recompute_weights_from_degree()
        # Heat the new node (and its one edge neighbor) so it re-anneals
        # while the rest of the converged graph stays cool.
        node_temperature.resize(dom.n)
        initial_temp = config.physics.initial_temperature
        current_temp = max(temperature.get(), config.physics.min_temperature)
        heat_val = initial_temp / current_temp
        affected = [dom.n - 1]
        if neighbor is not None:
            affected.append(neighbor)
        node_temperature.heat_nodes(affected, heat_val)

    mutate.queue(_action)
