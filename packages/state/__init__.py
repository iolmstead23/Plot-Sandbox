"""state: app-wide mutable state. Fully atomized — no internal-package imports."""

from .app_state import AppState, state

__all__ = ["AppState", "state"]
