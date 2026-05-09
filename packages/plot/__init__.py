"""plot: matplotlib-based 3D figure builders. Accepts plain primitives and NumPy arrays only."""

from .scatter_3d import Artists, build_scatter_3d_figure, update_scatter_3d

__all__ = [
    "Artists",
    "build_scatter_3d_figure",
    "update_scatter_3d",
]
