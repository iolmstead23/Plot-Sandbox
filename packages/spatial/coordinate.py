"""Coordinate dataclass: the output shape returned by every formula."""

from dataclasses import dataclass


@dataclass
class Coordinate:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
