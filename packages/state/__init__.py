"""state: app-wide mutable state. Fully atomized — no internal-package imports."""

from .app_state import AppState, state
from .knowledge_graph import SAMPLE_EDGES, SAMPLE_LABELS, SAMPLE_WEIGHTS

__all__ = [
    "AppState",
    "SAMPLE_EDGES",
    "SAMPLE_LABELS",
    "SAMPLE_WEIGHTS",
    "state",
]
