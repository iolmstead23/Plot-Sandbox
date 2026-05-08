"""Formula registry: each entry exposes the same compute(Element) -> Coordinate signature."""

from .formula_linear import compute as linear
from .formula_weighted import compute as weighted

__all__ = ["linear", "weighted"]
