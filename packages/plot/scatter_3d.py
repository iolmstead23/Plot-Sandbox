"""3D plot builder. RGB unit-axis vectors plus data scatter, with both a one-shot
build path (`build_scatter_3d_figure`) and an in-place update path
(`update_scatter_3d`) so the physics tick can mutate the scene without tearing
down the canvas.

All view and style parameters are supplied by the caller via `view_format` and
`plot_style` dicts — nothing is hardcoded here.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d  # type: ignore # noqa: F401  (registers '3d' projection)
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Text3D


class _UprightText(Text3D):
    """Text3D that always renders screen-horizontal — overrides view-angle rotation."""
    def get_rotation(self) -> float:
        return 0.0


@dataclass
class Artists:
    figure: Figure
    ax: Any
    scatter: Any                 # Path3DCollection
    edge_lines: Line3DCollection
    label_texts: list = field(default_factory=list)


def _strip_axis_chrome(ax) -> None:
    transparent = (1.0, 1.0, 1.0, 0.0)
    ax.grid(False)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color(transparent)
        axis.line.set_color(transparent)
        axis.label.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")


def _install_camera_clamp(
    figure: Figure,
    ax,
    *,
    elev_min: float,
    elev_max: float,
) -> None:
    def clamp(event):
        if event.inaxes is not ax or event.button != 1:
            return
        needs_redraw = False
        if ax.elev < elev_min:
            ax.elev = elev_min
            needs_redraw = True
        elif ax.elev > elev_max:
            ax.elev = elev_max
            needs_redraw = True
        if getattr(ax, "roll", 0.0) != 0.0:
            ax.roll = 0.0
            needs_redraw = True
        if needs_redraw:
            figure.canvas.draw_idle()

    figure.canvas.mpl_connect("motion_notify_event", clamp)


def build_scatter_3d_figure(
    positions: np.ndarray,
    sizes: np.ndarray,
    labels: list[str],
    edges: np.ndarray,
    *,
    view_format: dict,
    plot_style: dict,
    title: str = "3D Plot",
    focus: tuple[float, float, float] = (0.0, 0.0, 0.0),
    depthshade: bool = False,
) -> tuple[Figure, Artists]:
    figsize = plot_style["figsize"]
    figure = Figure(figsize=(figsize[0], figsize[1]))
    ax = figure.add_subplot(111, projection="3d")
    _strip_axis_chrome(ax)

    fx, fy, fz = focus
    arrow = view_format["axis_length"]
    alr = plot_style["arrow_length_ratio"]
    qlw = plot_style["quiver_linewidth"]
    qa  = plot_style["quiver_alpha"]
    ax.quiver(fx, fy, fz, arrow, 0, 0, color="red",   arrow_length_ratio=alr, linewidth=qlw, alpha=qa)
    ax.quiver(fx, fy, fz, 0, arrow, 0, color="green", arrow_length_ratio=alr, linewidth=qlw, alpha=qa)
    ax.quiver(fx, fy, fz, 0, 0, arrow, color="blue",  arrow_length_ratio=alr, linewidth=qlw, alpha=qa)

    size_scale = plot_style["size_scale"]
    if positions.shape[0] > 0:
        xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]
        scatter_sizes = sizes * size_scale
    else:
        xs = ys = zs = np.zeros(0)
        scatter_sizes = np.zeros(0)
    scatter = ax.scatter(
        xs, ys, zs,  # type: ignore[arg-type]
        c="tab:blue",
        s=scatter_sizes,  # type: ignore[arg-type]
        depthshade=depthshade,
    )

    if edges.shape[0] > 0:
        segs = positions[edges]
    else:
        segs = np.zeros((0, 2, 3))
    edge_lines = Line3DCollection(segs, colors="black", linewidths=plot_style["edge_linewidth"])
    ax.add_collection3d(edge_lines)

    offset = view_format["label_offset"]
    fontsize = plot_style["label_fontsize"]
    label_texts = []
    for i, label in enumerate(labels):
        if i < positions.shape[0]:
            x, y, z = positions[i]
        else:
            x, y, z = 0.0, 0.0, 0.0
        t = ax.text(
            float(x), float(y), float(z) + offset,
            label, ha="center", va="center", fontsize=fontsize,
        )
        t.__class__ = _UprightText
        label_texts.append(t)

    ax.set_title(title)

    R = view_format["view_range"]
    ax.set_xlim(fx - R, fx + R)
    ax.set_ylim(fy - R, fy + R)
    ax.set_zlim(fz - R, fz + R)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.set_autoscale_on(False)

    ax.view_init(
        elev=view_format["elev"],
        azim=view_format["azim"],
        roll=view_format["roll"],
    )
    _install_camera_clamp(
        figure, ax,
        elev_min=view_format["elev_min"],
        elev_max=view_format["elev_max"],
    )

    figure.tight_layout()

    return figure, Artists(
        figure=figure,
        ax=ax,
        scatter=scatter,
        edge_lines=edge_lines,
        label_texts=label_texts,
    )


def update_scatter_3d(
    artists: Artists,
    positions: np.ndarray,
    sizes: np.ndarray,
    edges: np.ndarray,
    labels: Optional[list[str]] = None,
    *,
    view_format: dict,
    plot_style: dict,
) -> None:
    """Mutate existing artists in place. Caller schedules canvas.draw_idle()."""
    n = positions.shape[0]
    size_scale = plot_style["size_scale"]
    offset = view_format["label_offset"]
    fontsize = plot_style["label_fontsize"]

    artists.scatter._offsets3d = (
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
    )
    artists.scatter.set_sizes(sizes * size_scale)

    if edges.shape[0] > 0:
        segs = positions[edges]
    else:
        segs = np.zeros((0, 2, 3))
    artists.edge_lines.set_segments(list(segs))  # type: ignore[arg-type]

    if labels is not None:
        while len(artists.label_texts) < n:
            i = len(artists.label_texts)
            x, y, z = positions[i]
            t = artists.ax.text(
                float(x), float(y), float(z) + offset,
                labels[i], ha="center", va="center", fontsize=fontsize,
            )
            t.__class__ = _UprightText
            artists.label_texts.append(t)

    for i, t in enumerate(artists.label_texts):
        if i >= n:
            t.set_visible(False)
            continue
        x, y, z = positions[i]
        t.set_visible(True)
        t.set_position((float(x), float(y)))
        t.set_3d_properties(float(z) + offset, "z")
        if labels is not None and i < len(labels):
            t.set_text(labels[i])

