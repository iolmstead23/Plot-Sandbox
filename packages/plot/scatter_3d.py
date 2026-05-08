"""3D plot builder. Renders X/Y/Z RGB unit-axis vectors plus data scatter."""

from matplotlib.figure import Figure
from mpl_toolkits import mplot3d  # type: ignore # noqa: F401  (registers the '3d' projection)


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


def _install_camera_clamp(figure: Figure, ax) -> None:
    from . import VIEW_FORMAT

    elev_min = VIEW_FORMAT["elev_min"]
    elev_max = VIEW_FORMAT["elev_max"]

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
        # Up-vector flip guard: never let roll drift from 0.
        if getattr(ax, "roll", 0.0) != 0.0:
            ax.roll = 0.0
            needs_redraw = True
        if needs_redraw:
            figure.canvas.draw_idle()

    figure.canvas.mpl_connect("motion_notify_event", clamp)


def build_scatter_3d_figure(
    points: list[tuple[str, float, float, float]],
    *,
    edges: list[tuple[str, str]] | None = None,
    title: str = "3D Plot of Elements",
    focus: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> Figure:
    from . import VIEW_FORMAT

    figure = Figure(figsize=(8, 6))
    ax = figure.add_subplot(111, projection="3d")

    _strip_axis_chrome(ax)

    fx, fy, fz = focus
    arrow = VIEW_FORMAT["axis_length"]

    # Vectors originate at the focus and extend past view_range so that the
    # shafts remain visible from any orbit angle / clamp position.
    ax.quiver(fx, fy, fz, arrow, 0, 0, color="red", arrow_length_ratio=0.02)
    ax.quiver(fx, fy, fz, 0, arrow, 0, color="green", arrow_length_ratio=0.02)
    ax.quiver(fx, fy, fz, 0, 0, arrow, color="blue", arrow_length_ratio=0.02)

    xs = [p[1] for p in points]
    ys = [p[2] for p in points]
    zs = [p[3] for p in points]
    ax.scatter(xs, ys, zs, c="tab:blue", s=60, depthshade=True)

    if edges:
        coords = {p[0]: (p[1], p[2], p[3]) for p in points}
        for a, b in edges:
            ax_, ay_, az_ = coords[a]
            bx_, by_, bz_ = coords[b]
            ax.plot([ax_, bx_], [ay_, by_], [az_, bz_], color="black", linewidth=0.5)

    offset = VIEW_FORMAT["label_offset"]
    for label, x, y, z in points:
        ax.text(x, y, z + offset, label, ha="center", va="center", fontsize=10)

    ax.set_title(title)

    # Lock the view box symmetrically around the focus so origin (or whatever
    # focus is set to) sits at the center of the screen and stays there as
    # the user orbits.
    R = VIEW_FORMAT["view_range"]
    ax.set_xlim(fx - R, fx + R)
    ax.set_ylim(fy - R, fy + R)
    ax.set_zlim(fz - R, fz + R)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.set_autoscale_on(False)

    ax.view_init(
        elev=VIEW_FORMAT["elev"],
        azim=VIEW_FORMAT["azim"],
        roll=VIEW_FORMAT["roll"],
    )

    _install_camera_clamp(figure, ax)

    figure.tight_layout()
    return figure


def show(figure: Figure) -> None:
    figure.show()
