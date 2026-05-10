import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import initial_layout


def seed_physics_dom(rng: np.random.Generator) -> None:
    dom.clear()
    sim = config.simulation
    n = sim.node_count

    # Build a random undirected graph: each node tries to connect to
    # k random peers where k ~ Uniform[1, max_degree].
    edges: set[tuple[int, int]] = set()
    for i in range(n):
        k = int(rng.integers(1, sim.max_degree + 1))
        candidates = np.delete(np.arange(n), i)
        targets = rng.choice(candidates, size=min(k, len(candidates)), replace=False)
        for t in targets:
            a, b = (i, int(t)) if i < int(t) else (int(t), i)
            edges.add((a, b))

    # Derive initial weights from degree so heavier nodes have more connections.
    degrees = np.zeros(n, dtype=np.float64)
    for a, b in edges:
        degrees[a] += 1.0
        degrees[b] += 1.0
    raw = np.maximum(degrees, 1.0)
    w_lo, w_hi = float(raw.min()), float(raw.max())
    if w_hi > w_lo:
        weights = sim.weight_min + (raw - w_lo) / (w_hi - w_lo) * (
            sim.weight_max - sim.weight_min
        )
    else:
        weights = np.full(n, (sim.weight_min + sim.weight_max) / 2.0, dtype=np.float64)

    positions = initial_layout(
        weights,
        view_range=config.view.view_range,
        rng=rng,
        inner_radius_fraction=sim.inner_radius_fraction,
        outer_radius_fraction=sim.outer_radius_fraction,
        dims=sim.dims,
    )

    for i in range(n):
        dom.add_node(float(weights[i]), positions[i])

    for a, b in sorted(edges):
        dom.add_edge(a, b)
