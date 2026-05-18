"""Default configuration values used when config.json is absent.

Values here must stay in sync with config.json so that a first-run user
gets the same behaviour as an existing user whose config.json was written
by a prior version of the app.
"""

_DEFAULT_CONFIG: dict = {
    "physics": {
        "gravity_ratio": 0.001,
        "repel_ratio": 0.004,
        "k_attract": 0.5,
        "soft_core_radius": 0.6,
        "max_step": 0.4,
        "F_max": 200.0,
        "focus": [0.0, 0.0, 0.0],
        "initial_temperature": 1.0,
        "cooling_factor": 0.999,
        "min_temperature": 0.0001,
        "k_edge": 0.0001,
        "edge_rest_length": 5.0,
        "repulsion_cutoff": 3.0,
        "bh_threshold": 5000,
        "bh_theta": 0.7,
        "mutation_reheat_factor": 0.05,
        "cpu_sparse_threshold": 150,
    },
    "simulation": {
        "node_count": 2500,
        "weight_min": 1.0,
        "weight_max": 50.0,
        "spawn_distance": 2.0,
        "inner_radius_fraction": 0.1,
        "outer_radius_fraction": 0.9,
        "dims": 3,
        "max_degree": 10,
        "use_gpu": True,
        "layout_noise": 1.0,
        "gpu_memory_pool_gb": 4.0,
    },
    "tick": {
        "dt": 0.05,
        "equilibrium_threshold": 0.0025,
        "interval_ms": 33,
        "render_every": 2,
        "physics_substeps": 32,
        "cuda_device": 0,
        "stats_interval": 1.0,
        "headless_max_ticks": 50000,
    },
    "render": {
        "camera_elev": 25.0,
        "camera_azim": -60.0,
        "view_range": 10.0,
        "camera_distance": 30.0,
        "title": "Knowledge Graph Simulation",
        "size_scale": 1.0,
        "node_size_min": 2.0,
        "node_size_max": 20.0,
        "weight_to_size": 3.0,
    },
    "ui": {
        "window_title": "3D Plot",
        "geometry": "1920x1080",
        "button_padx": 8,
        "button_pady": 6,
    },
    "velocimetry": {
        "enabled": True,
        "output_path": "output",
        "save_csv": False,
        "save_npz": True,
        "plot_on_convergence": True,
        "max_frames": 20000,
    },
    "sliders": {
        "gravity_ratio": {"min": 0.0, "max": 0.01, "step": 0.0001},
        "repel_ratio": {"min": 0.0, "max": 0.05, "step": 0.0005},
        "k_edge": {"min": 0.0, "max": 1.0, "step": 0.01},
    },
}
