from dataclasses import dataclass


@dataclass
class TickConfig:
    dt: float
    equilibrium_threshold: float
    interval_ms: int
    render_every: int = 1
    physics_substeps: int = 8
    cuda_device: int = 0
    stats_interval: float = 1.0
    headless_max_ticks: int = 50000
