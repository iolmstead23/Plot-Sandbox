from dataclasses import dataclass


@dataclass
class SimulationConfig:
    node_count: int
    weight_min: float
    weight_max: float
    spawn_distance: float
    inner_radius_fraction: float
    outer_radius_fraction: float
    dims: int
    max_degree: int = 6
    use_gpu: bool = True
    layout_noise: float = 1.0
