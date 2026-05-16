from dataclasses import dataclass


@dataclass
class ViewConfig:
    elev: float
    azim: float
    view_range: float
    camera_distance: float = 30.0
