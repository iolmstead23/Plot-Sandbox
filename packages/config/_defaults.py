"""Default configuration values for config.json."""

_DEFAULT_CONFIG: dict = {
    "physics": {
        "k_central": 2.0,
        "k_repel": 10.0,
        "k_attract": 0.8,
        "soft_core_radius": 0.6,
        "max_step": 0.4,
        "F_max": 200.0,
        "focus": [0.0, 0.0, 0.0],
        "initial_temperature": 1.0,
        "cooling_factor": 0.98,
        "min_temperature": 0.05,
        "k_edge": 0.08,
        "edge_rest_length": 5.0,
        "repulsion_cutoff": 6.0,
    },
    "simulation": {
        "node_count": 30,
        "weight_min": 0.5,
        "weight_max": 3.0,
        "spawn_distance": 4.0,
        "inner_radius_fraction": 0.1,
        "outer_radius_fraction": 0.9,
        "dims": 3,
        "max_degree": 6,
        "use_gpu": True,
    },
    "tick": {
        "dt": 0.05,
        "equilibrium_threshold": 0.001,
        "interval_ms": 33,
        "render_every": 1,
        "physics_substeps": 8,
    },
    "view": {
        "elev": 25.0,
        "azim": -60.0,
        "view_range": 10.0,
    },
    "plot": {
        "title": "Knowledge Graph Simulation",
        "size_scale": 1.0,
    },
    "dom": {
        "weight_to_size": 40.0,
    },
    "ui": {
        "window_title": "3D Plot",
        "geometry": "900x600",
        "button_padx": 8,
        "button_pady": 6,
    },
}
