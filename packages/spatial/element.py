"""Element dataclass: the input shape for all coordinate formulas."""

from dataclasses import dataclass


# Additional attributes will be added in a later pass.
@dataclass
class Element:
    label: str
    weight: float
    token_count: int
    backlink_count: int
