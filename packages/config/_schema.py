# Maps each key to its expected Python type(s). Lists validated separately.
_SCHEMA: dict = {
    "physics": {
        "k_central": (int, float),
        "k_repel": (int, float),
        "k_attract": (int, float),
        "soft_core_radius": (int, float),
        "max_step": (int, float),
        "F_max": (int, float),
        "focus": list,
        "initial_temperature": (int, float),
        "cooling_factor": (int, float),
        "min_temperature": (int, float),
        "k_edge": (int, float),
        "edge_rest_length": (int, float),
        "repulsion_cutoff": (int, float),
    },
    "simulation": {
        "node_count": int,
        "weight_min": (int, float),
        "weight_max": (int, float),
        "spawn_distance": (int, float),
        "inner_radius_fraction": (int, float),
        "outer_radius_fraction": (int, float),
        "dims": int,
        "max_degree": int,
        "use_gpu": bool,
    },
    "tick": {
        "dt": (int, float),
        "equilibrium_threshold": (int, float),
        "interval_ms": int,
        "render_every": int,
        "physics_substeps": int,
    },
    "view": {
        "elev": (int, float),
        "azim": (int, float),
        "view_range": (int, float),
    },
    "plot": {
        "title": str,
        "size_scale": (int, float),
    },
    "dom": {
        "weight_to_size": (int, float),
    },
    "ui": {
        "window_title": str,
        "geometry": str,
        "button_padx": int,
        "button_pady": int,
    },
}
