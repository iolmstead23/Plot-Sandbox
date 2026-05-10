"""state: app-wide mutable state. Fully atomized — no internal-package imports."""

from .app_state import state

__all__ = ["state"]
