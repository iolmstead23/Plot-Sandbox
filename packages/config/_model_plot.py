from dataclasses import dataclass


@dataclass
class PlotConfig:
    title: str
    size_scale: float
    node_size_min: float = 2.0
    node_size_max: float = 20.0
