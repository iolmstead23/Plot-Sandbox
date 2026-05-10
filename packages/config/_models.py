"""Typed dataclasses for every config.json section."""

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


@dataclass
class SimulationConfig:
    node_count: int
    weight_min: float
    weight_max: float
    spawn_distance: float
    inner_radius_fraction: float
    outer_radius_fraction: float
    dims: int
    max_degree: int = 6
    use_gpu: bool = True


@dataclass
class TickConfig:
    dt: float
    equilibrium_threshold: float
    interval_ms: int
    render_every: int = 1
    physics_substeps: int = 8


@dataclass
class ViewConfig:
    elev: float
    azim: float
    view_range: float


@dataclass
class PlotConfig:
    title: str
    size_scale: float


@dataclass
class DomConfig:
    weight_to_size: float


@dataclass
class UiConfig:
    window_title: str
    geometry: str
    button_padx: int
    button_pady: int


@dataclass
class Config:
    physics: PhysicsConfig
    simulation: SimulationConfig
    tick: TickConfig
    view: ViewConfig
    plot: PlotConfig
    dom: DomConfig
    ui: UiConfig
