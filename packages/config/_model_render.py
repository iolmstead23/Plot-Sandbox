from dataclasses import dataclass


@dataclass
class RenderConfig:
    camera_elev: float
    camera_azim: float
    view_range: float
    camera_distance: float
    title: str
    size_scale: float
    node_size_min: float
    node_size_max: float
    weight_to_size: float
