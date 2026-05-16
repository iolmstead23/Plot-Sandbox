from dataclasses import dataclass

from ._model_dom import DomConfig
from ._model_physics import PhysicsConfig
from ._model_plot import PlotConfig
from ._model_simulation import SimulationConfig
from ._model_tick import TickConfig
from ._model_ui import UiConfig
from ._model_velocimetry import VelocimetryConfig
from ._model_view import ViewConfig


@dataclass
class Config:
    physics: PhysicsConfig
    simulation: SimulationConfig
    tick: TickConfig
    view: ViewConfig
    plot: PlotConfig
    dom: DomConfig
    ui: UiConfig
    velocimetry: VelocimetryConfig
