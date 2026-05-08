"""Handler for the Weighted button: apply the weighted spatial formula to the seed records."""

from packages.plot import build_scatter_3d_figure
from packages.spatial import formulas
from packages.state import SAMPLE_ELEMENT_RECORDS, state

from ._compute import points_from_formula


def show_weighted(app) -> None:
    points = points_from_formula(SAMPLE_ELEMENT_RECORDS, formulas.weighted)
    state.set_points(points, title="Weighted formula")
    figure = build_scatter_3d_figure(state.points, title=state.title, focus=state.camera_focus)
    app.set_figure(figure)
