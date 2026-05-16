from dataclasses import dataclass
from typing import List


@dataclass
class PhysicsConfig:
    gravity_ratio: float
    repel_ratio: float
    k_attract: float
    soft_core_radius: float
    max_step: float
    F_max: float
    focus: List[float]
    initial_temperature: float
    cooling_factor: float
    min_temperature: float
    k_edge: float
    edge_rest_length: float
    repulsion_cutoff: float = 6.0
    bh_threshold: int = 5000
    bh_theta: float = 0.7
    mutation_reheat_factor: float = 0.25
