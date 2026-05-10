"""Public type aliases for UI handler signatures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .app import App

ButtonHandler = Callable[["App"], None]
ButtonSpec = tuple[str, ButtonHandler]
SliderCallback = Callable[["App", float], None]
SliderSpec = tuple[str, float, float, float, float, SliderCallback]
