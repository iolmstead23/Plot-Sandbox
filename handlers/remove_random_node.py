"""Enqueue a remove_node mutation for a random existing node."""

import numpy as np

from packages.dom import dom

from . import mutate


_rng = np.random.default_rng()


def remove_random_node(app) -> None:
    ids = dom.ids()
    if not ids:
        return
    target = ids[int(_rng.integers(0, len(ids)))]
    mutate.queue_remove_node(target)
