"""Entry point: orchestrates spatial, state, plot, and ui packages."""

import argparse

from packages.plot import build_scatter_3d_figure, show
from packages.spatial import formulas
from packages.state import (
    SAMPLE_ELEMENT_RECORDS,
    generate_sample_points,
    sample_size,
    state,
)
from packages.ui import launch

from handlers import BUTTON_HANDLERS, points_from_formula


def main() -> None:
    parser = argparse.ArgumentParser(description="3D plot of elements.")
    parser.add_argument(
        "--source",
        choices=["sample", "linear", "weighted"],
        default="sample",
        help="Initial data source. In GUI mode, sidebar buttons can switch this at runtime.",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Open a standalone matplotlib window (no buttons) instead of the tkinter UI.",
    )
    args = parser.parse_args()

    if args.source == "sample":
        state.set_points(generate_sample_points(), title="Sample data")
    elif args.source == "linear":
        state.set_points(
            points_from_formula(SAMPLE_ELEMENT_RECORDS, formulas.linear),
            title="Linear formula",
        )
    else:
        state.set_points(
            points_from_formula(SAMPLE_ELEMENT_RECORDS, formulas.weighted),
            title="Weighted formula",
        )

    figure = build_scatter_3d_figure(
        state.points,
        edges=state.edges,
        title=state.title,
        focus=state.camera_focus,
    )

    if args.cli:
        show(figure)
    else:
        launch(figure, buttons=BUTTON_HANDLERS, sample_size=sample_size)


if __name__ == "__main__":
    main()
