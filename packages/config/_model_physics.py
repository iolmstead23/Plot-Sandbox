from dataclasses import dataclass
from typing import List


@dataclass
class PhysicsConfig:
    k_central: float
    k_repel: float
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
