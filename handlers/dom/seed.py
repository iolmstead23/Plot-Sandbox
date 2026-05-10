import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import initial_layout
from packages.state import SAMPLE_EDGES, SAMPLE_LABELS, SAMPLE_WEIGHTS


def seed_physics_dom(rng: np.random.Generator) -> None:
    dom.clear()
    sim = config.simulation

    # Rescale degree-based graph weights to span [weight_min, weight_max] so
    # the config range actually controls variance for the initial layout.
    graph_weights = np.asarray(SAMPLE_WEIGHTS, dtype=np.float64)
    w_lo, w_hi = graph_weights.min(), graph_weights.max()
    if w_hi > w_lo:
        graph_weights = sim.weight_min + (graph_weights - w_lo) / (w_hi - w_lo) * (
            sim.weight_max - sim.weight_min
        )
    else:
        graph_weights = np.full_like(
            graph_weights, (sim.weight_min + sim.weight_max) / 2.0
        )

    n_graph = len(SAMPLE_LABELS)
    n_extra = max(0, sim.node_count - n_graph)
    extra_weights = (
        rng.uniform(sim.weight_min, sim.weight_max, size=n_extra).astype(np.float64)
        if n_extra > 0
        else np.empty(0, dtype=np.float64)
    )
    all_weights = np.concatenate([graph_weights, extra_weights])

    positions = initial_layout(
        all_weights,
        view_range=config.view.view_range,
        rng=rng,
        inner_radius_fraction=sim.inner_radius_fraction,
        outer_radius_fraction=sim.outer_radius_fraction,
        dims=sim.dims,
    )

    label_to_index: dict[str, int] = {}
    for i, label in enumerate(SAMPLE_LABELS):
        dom.add_node(float(all_weights[i]), positions[i], label)
        label_to_index[label] = i

    for i in range(n_extra):
        dom.add_node(float(extra_weights[i]), positions[n_graph + i])

    for a, b in SAMPLE_EDGES:
        if a in label_to_index and b in label_to_index:
            dom.add_edge(label_to_index[a], label_to_index[b])
