from dataclasses import dataclass

from ._model_physics import PhysicsConfig
from ._model_render import RenderConfig
from ._model_simulation import SimulationConfig
from ._model_sliders import SlidersConfig
from ._model_tick import TickConfig
from ._model_ui import UiConfig
from ._model_velocimetry import VelocimetryConfig


@dataclass
class Config:
    physics: PhysicsConfig
    simulation: SimulationConfig
    tick: TickConfig
    render: RenderConfig
    ui: UiConfig
    velocimetry: VelocimetryConfig
    sliders: SlidersConfig
