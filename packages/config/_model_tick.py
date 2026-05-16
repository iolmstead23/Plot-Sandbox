from dataclasses import dataclass


@dataclass
class TickConfig:
    dt: float
    equilibrium_threshold: float
    interval_ms: int
    render_every: int = 1
    physics_substeps: int = 8
    cuda_device: int = 0
