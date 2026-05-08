"""Handler for the Sample button: generate a fresh set of random sample points."""

from packages.plot import build_scatter_3d_figure
from packages.state import generate_sample_points, state


def show_sample(app) -> None:
    points = generate_sample_points()
    state.set_points(points, title="Sample data")
    figure = build_scatter_3d_figure(
        state.points,
        edges=state.edges,
        title=state.title,
        focus=state.camera_focus,
    )
    app.set_figure(figure)
