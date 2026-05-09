"""Re-roll every node's weight uniformly in [weight_min, weight_max]. Reheat is handled
by the dom.on_change cascade wired in handlers/tick.py.
"""

import numpy as np

from packages.config import config
from packages.dom import dom

from . import mutate


_rng = np.random.default_rng()


def randomize_weights(app) -> None:
    sim = config.simulation
    for node_id in dom.ids():
        mutate.queue_set_weight(node_id, float(_rng.uniform(sim.weight_min, sim.weight_max)))
