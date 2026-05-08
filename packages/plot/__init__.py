"""plot: matplotlib-based 3D figure builders. Accepts plain primitives only."""

# Camera preset and rotation clamp bounds consumed by build_scatter_3d_figure.
# Edit here to retune the default view; the clamp values cap mouse rotation.
VIEW_FORMAT = {
    "elev": 25.0,
    "azim": -60.0,
    "roll": 0.0,
    "elev_min": -75.0,
    "elev_max":  75.0,
    "view_range": 5.0,       # half-extent of visible volume around camera_focus
    "axis_length": 50.0,     # RGB vector length; > view_range so vectors stay visible past the camera frustum
    "label_offset": 0.8,     # vertical screen-space offset (in points) to keep text above data points and avoid overlap
}

from .scatter_3d import build_scatter_3d_figure, show

__all__ = ["VIEW_FORMAT", "build_scatter_3d_figure", "show"]
