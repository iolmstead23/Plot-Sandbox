from dataclasses import dataclass


@dataclass
class ViewConfig:
    elev: float
    azim: float
    view_range: float
