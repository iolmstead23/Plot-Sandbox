import numpy as np

from packages.dom import dom

from . import mutate
from .weights import recompute_weights_from_degree
from ..state import node_temperature

_rng = np.random.default_rng()


def remove_random_node(_app) -> None:
    ids = dom.ids()
    if not ids:
        return
    target = ids[int(_rng.integers(0, len(ids)))]

    def _action() -> None:
        dom.remove_node(target)
        recompute_weights_from_degree()
        node_temperature.resize(dom.n)

    mutate.queue(_action)
