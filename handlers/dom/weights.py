import numpy as np

from packages.config import config
from packages.dom import dom


def recompute_weights_from_degree() -> None:
    """Set each node's weight to its undirected edge degree, rescaled to [weight_min, weight_max].

    Isolated nodes (degree 0) get a floor of 1 so they remain visible.
    Writes to dom.weights in a single batch then emits one revision bump.
    """
    if dom.n == 0:
        return
    sim = config.simulation
    degrees = np.zeros(dom.n, dtype=np.float64)
    for a, b in dom.edges:
        degrees[int(a)] += 1.0
        degrees[int(b)] += 1.0
    raw = np.maximum(degrees, 1.0)
    w_lo, w_hi = float(raw.min()), float(raw.max())
    if w_hi > w_lo:
        weights = sim.weight_min + (raw - w_lo) / (w_hi - w_lo) * (
            sim.weight_max - sim.weight_min
        )
    else:
        weights = np.full(
            dom.n, (sim.weight_min + sim.weight_max) / 2.0, dtype=np.float64
        )
    dom.weights[:] = weights
    dom._bump(positions_changed=False)
