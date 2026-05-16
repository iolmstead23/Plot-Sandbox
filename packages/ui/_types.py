"""Public type aliases for UI handler signatures."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ._app import App

ButtonHandler = Callable[["App"], None]
# ButtonSpec is either (label, handler) or (label, handler, gated_by_convergence).
# When the third element is True the button is disabled until the simulation
# converges and re-enabled each time it converges again.
ButtonSpec = tuple[str, ButtonHandler] | tuple[str, ButtonHandler, bool]
SliderCallback = Callable[["App", float], None]
SliderSpec = tuple[str, float, float, float, float, SliderCallback]
