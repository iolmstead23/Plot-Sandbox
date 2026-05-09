"""Seed a fresh physics DOM. Shared by main.py startup and the New Sim button."""

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import initial_layout
from packages.plot import build_scatter_3d_figure, project_to_3d
from packages.state import SAMPLE_EDGES, SAMPLE_LABELS, SAMPLE_WEIGHTS, state

from .tick import physics_tick


def seed_physics_dom(rng: np.random.Generator) -> None:
    """Clear DOM and populate from the static sample knowledge graph."""
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


def reseed(app) -> None:
    app.stop_tick()

    seed_physics_dom(np.random.default_rng())

    figure, artists = build_scatter_3d_figure(
        project_to_3d(dom.positions),
        dom.sizes,
        list(dom.labels),
        dom.edges,
        view_format=vars(config.view),
        plot_style=vars(config.plot),
        title=config.plot.title,
        focus=state.camera_focus,
        depthshade=False,
    )
    app.set_figure(figure)
    app.set_artists(artists)
    app.update_banner(dom.n)
    app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)
