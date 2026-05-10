"""Application configuration — single source of truth for all hyperparameters.

Loads config.json from the project root on first import and exposes a typed
`config` singleton. If config.json is absent it is auto-generated with defaults.
No sibling packages are imported here.
"""

from ._models import (
    Config,
    DomConfig,
    PhysicsConfig,
    PlotConfig,
    SimulationConfig,
    TickConfig,
    UiConfig,
    ViewConfig,
)
from ._loader import load_config

__all__ = [
    "Config",
    "DomConfig",
    "PhysicsConfig",
    "PlotConfig",
    "SimulationConfig",
    "TickConfig",
    "UiConfig",
    "ViewConfig",
    "config",
    "load_config",
]

# Module-level singleton — loaded once at import time.
config: Config = load_config()
