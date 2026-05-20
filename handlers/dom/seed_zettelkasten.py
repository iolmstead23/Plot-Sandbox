import numpy as np

from packages.dom import dom
from packages.physics import initial_layout
from packages.config import config
from packages.zettelkasten.scanner import scan_directory
from packages.zettelkasten.linker import build_edges
from packages.zettelkasten.weights import compute_weights


def seed_from_zettelkasten(path: str, rng: np.random.Generator) -> None:
    notes = scan_directory(path)
    if not notes:
        raise ValueError(f'No markdown files found in {path!r}')

    sim = config.simulation
    weights = compute_weights(notes, sim.weight_min, sim.weight_max)
    edges = build_edges(notes)
    weights_arr = np.array(weights, dtype=np.float64)

    positions = initial_layout(
        weights_arr,
        view_range=config.render.view_range,
        rng=rng,
        inner_radius_fraction=sim.inner_radius_fraction,
        outer_radius_fraction=sim.outer_radius_fraction,
        dims=sim.dims,
        layout_noise=sim.layout_noise,
    )

    dom.clear()
    for i, note in enumerate(notes):
        dom.add_node(float(weights[i]), positions[i], note.label)
    for a, b in edges:
        dom.add_edge(a, b)
