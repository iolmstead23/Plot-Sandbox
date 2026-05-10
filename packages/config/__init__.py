"""Application configuration — single source of truth for all hyperparameters.

Loads config.json from the project root on first import and exposes a typed
`config` singleton. If config.json is absent it is auto-generated with defaults.
No sibling packages are imported here.
"""

import json
import os
from dataclasses import asdict, dataclass
from typing import List

# ---------------------------------------------------------------------------
# Dataclasses (one per JSON section)
# ---------------------------------------------------------------------------


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


@dataclass
class SimulationConfig:
    node_count: int
    weight_min: float
    weight_max: float
    spawn_distance: float
    inner_radius_fraction: float
    outer_radius_fraction: float
    dims: int


@dataclass
class TickConfig:
    attraction_radius: float
    dt: float
    equilibrium_threshold: float
    interval_ms: int


@dataclass
class ViewConfig:
    elev: float
    azim: float
    roll: float
    elev_min: float
    elev_max: float
    view_range: float
    axis_length: float
    label_offset: float


@dataclass
class PlotConfig:
    title: str
    figsize: List[float]
    size_scale: float
    arrow_length_ratio: float
    quiver_linewidth: float
    quiver_alpha: float
    label_fontsize: int
    label_alpha: float
    label_color: str
    label_stroke_width: float
    edge_linewidth: float


@dataclass
class DomConfig:
    weight_to_size: float


@dataclass
class UiConfig:
    window_title: str
    geometry: str
    button_width: int
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


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_CONFIG: dict = {
    "physics": {
        "k_central": 2.0,
        "k_repel": 10.0,
        "k_attract": 0.8,
        "soft_core_radius": 0.6,
        "max_step": 0.4,
        "F_max": 200.0,
        "focus": [0.0, 0.0, 0.0],
        "initial_temperature": 1.0,
        "cooling_factor": 0.98,
        "min_temperature": 0.05,
        "k_edge": 0.08,
        "edge_rest_length": 5.0,
    },
    "simulation": {
        "node_count": 30,
        "weight_min": 0.5,
        "weight_max": 3.0,
        "spawn_distance": 4.0,
        "inner_radius_fraction": 0.1,
        "outer_radius_fraction": 0.9,
        "dims": 3,
    },
    "tick": {
        "attraction_radius": 2.5,
        "dt": 0.05,
        "equilibrium_threshold": 0.001,
        "interval_ms": 33,
    },
    "view": {
        "elev": 25.0,
        "azim": -60.0,
        "roll": 0.0,
        "elev_min": -75.0,
        "elev_max": 75.0,
        "view_range": 10.0,
        "axis_length": 50.0,
        "label_offset": 0.4,
    },
    "plot": {
        "title": "Knowledge Graph Simulation",
        "figsize": [10, 6],
        "size_scale": 1.0,
        "arrow_length_ratio": 0.02,
        "quiver_linewidth": 0.6,
        "quiver_alpha": 0.35,
        "label_fontsize": 10,
        "label_alpha": 0.85,
        "label_color": "#444444",
        "label_stroke_width": 2.5,
        "edge_linewidth": 0.5,
    },
    "dom": {
        "weight_to_size": 40.0,
    },
    "ui": {
        "window_title": "3D Plot",
        "geometry": "900x600",
        "button_width": 14,
        "button_padx": 8,
        "button_pady": 6,
    },
}

# ---------------------------------------------------------------------------
# Validation schema: maps each key to its expected Python type(s).
# Lists are validated separately (see _validate).
# ---------------------------------------------------------------------------

_SCHEMA: dict = {
    "physics": {
        "k_central": (int, float),
        "k_repel": (int, float),
        "k_attract": (int, float),
        "soft_core_radius": (int, float),
        "max_step": (int, float),
        "F_max": (int, float),
        "focus": list,  # validated for length/element type below
        "initial_temperature": (int, float),
        "cooling_factor": (int, float),
        "min_temperature": (int, float),
        "k_edge": (int, float),
        "edge_rest_length": (int, float),
    },
    "simulation": {
        "node_count": int,
        "weight_min": (int, float),
        "weight_max": (int, float),
        "spawn_distance": (int, float),
        "inner_radius_fraction": (int, float),
        "outer_radius_fraction": (int, float),
        "dims": int,
    },
    "tick": {
        "attraction_radius": (int, float),
        "dt": (int, float),
        "equilibrium_threshold": (int, float),
        "interval_ms": int,
    },
    "view": {
        "elev": (int, float),
        "azim": (int, float),
        "roll": (int, float),
        "elev_min": (int, float),
        "elev_max": (int, float),
        "view_range": (int, float),
        "axis_length": (int, float),
        "label_offset": (int, float),
    },
    "plot": {
        "title": str,
        "figsize": list,  # validated for length/element type below
        "size_scale": (int, float),
        "arrow_length_ratio": (int, float),
        "quiver_linewidth": (int, float),
        "quiver_alpha": (int, float),
        "label_fontsize": int,
        "label_alpha": (int, float),
        "label_color": str,
        "label_stroke_width": (int, float),
        "edge_linewidth": (int, float),
    },
    "dom": {
        "weight_to_size": (int, float),
    },
    "ui": {
        "window_title": str,
        "geometry": str,
        "button_width": int,
        "button_padx": int,
        "button_pady": int,
    },
}


def _type_name(t) -> str:
    if isinstance(t, tuple):
        return " | ".join(x.__name__ for x in t)
    return t.__name__


def _validate(data: dict) -> None:
    """Raise TypeError or KeyError with a descriptive path on any mismatch."""
    for section, fields in _SCHEMA.items():
        if section not in data:
            raise KeyError(f"Missing config section: '{section}'")
        sec = data[section]
        for key, expected in fields.items():
            if key not in sec:
                raise KeyError(f"Missing config key: '{section}.{key}'")
            value = sec[key]
            if not isinstance(value, expected):
                raise TypeError(
                    f"config.{section}.{key}: expected {_type_name(expected)}, "
                    f"got {type(value).__name__} ({value!r})"
                )

    # Extra structural checks for list fields.
    focus = data["physics"]["focus"]
    if len(focus) != 3 or not all(isinstance(v, (int, float)) for v in focus):
        raise TypeError("config.physics.focus must be a list of 3 numbers")

    figsize = data["plot"]["figsize"]
    if len(figsize) != 2 or not all(isinstance(v, (int, float)) for v in figsize):
        raise TypeError("config.plot.figsize must be a list of 2 numbers")

    if data["simulation"]["dims"] < 1:
        raise ValueError("config.simulation.dims must be >= 1")


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge override into a copy of base, section by section."""
    result = {k: dict(v) for k, v in base.items()}
    for section, fields in override.items():
        if section in result and isinstance(fields, dict):
            result[section].update(fields)
        else:
            result[section] = fields
    return result


def _dict_to_config(d: dict) -> Config:
    p = d["physics"]
    s = d["simulation"]
    t = d["tick"]
    v = d["view"]
    pl = d["plot"]
    dm = d["dom"]
    u = d["ui"]
    return Config(
        physics=PhysicsConfig(**p),
        simulation=SimulationConfig(**s),
        tick=TickConfig(**t),
        view=ViewConfig(**v),
        plot=PlotConfig(**pl),
        dom=DomConfig(**dm),
        ui=UiConfig(**u),
    )


def _config_to_dict(cfg: Config) -> dict:
    return {
        "physics": asdict(cfg.physics),
        "simulation": asdict(cfg.simulation),
        "tick": asdict(cfg.tick),
        "view": asdict(cfg.view),
        "plot": asdict(cfg.plot),
        "dom": asdict(cfg.dom),
        "ui": asdict(cfg.ui),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_config(path: str = "config.json") -> Config:
    """Load config from *path*, auto-generating it with defaults if absent.

    Deep-merges the file over defaults so new keys added in future versions
    of the app are always present even when the user's file is older.
    Raises TypeError or KeyError on type mismatches.
    """
    if not os.path.exists(path):
        data = _DEFAULT_CONFIG
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    else:
        with open(path, "r", encoding="utf-8") as fh:
            user_data = json.load(fh)
        data = _deep_merge(_DEFAULT_CONFIG, user_data)

    _validate(data)
    return _dict_to_config(data)


# Module-level singleton — loaded once at import time.
config: Config = load_config()
