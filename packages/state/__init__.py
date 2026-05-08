"""state: app-wide mutable state and seed data. Fully atomized — no internal-package imports."""

from .app_state import (
    AppState,
    SAMPLE_ELEMENT_RECORDS,
    generate_sample_points,
    sample_size,
    state,
)

__all__ = [
    "AppState",
    "SAMPLE_ELEMENT_RECORDS",
    "generate_sample_points",
    "sample_size",
    "state",
]
