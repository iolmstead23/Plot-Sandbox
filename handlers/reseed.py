"""Seed a fresh physics DOM. Shared by main.py startup and the New Sim button."""

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import initial_layout
from packages.plot import build_scatter_3d_figure
from packages.state import state

from .tick import physics_tick


def seed_physics_dom(rng: np.random.Generator) -> None:
    """Clear DOM and populate with a fresh random layout."""
    dom.clear()
    sim = config.simulation
    weights = rng.uniform(sim.weight_min, sim.weight_max, size=sim.node_count)
    positions = initial_layout(
        weights,
        view_range=config.view.view_range,
        rng=rng,
        inner_radius_fraction=sim.inner_radius_fraction,
        outer_radius_fraction=sim.outer_radius_fraction,
    )
    for i in range(sim.node_count):
        dom.add_node(float(weights[i]), positions[i])


def reseed(app) -> None:
    app.stop_tick()

    seed_physics_dom(np.random.default_rng())

    edges = dom.pairs_within_radius(config.tick.attraction_radius)
    figure, artists = build_scatter_3d_figure(
        dom.positions, dom.sizes, list(dom.labels), edges,
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
