import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import initial_layout
from packages.state import SAMPLE_EDGES, SAMPLE_LABELS, SAMPLE_WEIGHTS


def seed_physics_dom(rng: np.random.Generator) -> None:
    dom.clear()
    sim = config.simulation
    weights = np.asarray(SAMPLE_WEIGHTS, dtype=np.float64)
    positions = initial_layout(
        weights,
        view_range=config.view.view_range,
        rng=rng,
        inner_radius_fraction=sim.inner_radius_fraction,
        outer_radius_fraction=sim.outer_radius_fraction,
        dims=sim.dims,
    )
    label_to_index: dict[str, int] = {}
    for i, label in enumerate(SAMPLE_LABELS):
        dom.add_node(float(weights[i]), positions[i], label)
        label_to_index[label] = i
    for a, b in SAMPLE_EDGES:
        if a in label_to_index and b in label_to_index:
            dom.add_edge(label_to_index[a], label_to_index[b])
