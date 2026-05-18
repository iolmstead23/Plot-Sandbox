"""Application configuration — single source of truth for all hyperparameters.

Loads config.json from the project root on first import and exposes a typed
`config` singleton. If config.json is absent it is auto-generated with defaults.
No sibling packages are imported here.
"""

from ._loader import load_config, save_config
from ._model_root import Config

__all__ = ["config", "load_config", "save_config"]

# Module-level singleton — loaded once at import time.
config: Config = load_config()
