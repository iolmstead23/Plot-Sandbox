import numpy as np

_MAX_CURVES = 300  # matplotlib ceiling — 5000 curves * 20k pts each is impractical


def phase_plot(temperatures: np.ndarray, distances: np.ndarray, weights: np.ndarray):
    """Return a matplotlib Figure of phase curves colored by particle weight.

    Uses Figure directly (no pyplot) so it is safe to call from any thread.

    X-axis: temperature (inverted — high T on left, low T on right).
    Y-axis: distance from gravity focus.
    Color:  particle weight via plasma colormap.
    """
    import matplotlib
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.colorbar import ColorbarBase
    from matplotlib.colors import Normalize
    from matplotlib.figure import Figure

    n_particles = distances.shape[1]
    if n_particles > _MAX_CURVES:
        idx = np.linspace(0, n_particles - 1, _MAX_CURVES, dtype=int)
        distances = distances[:, idx]
        weights = weights[idx]
        n_particles = _MAX_CURVES

    fig = Figure(figsize=(14, 8))
    FigureCanvasAgg(fig)
    ax = fig.add_subplot(111)

    w_min, w_max = float(weights.min()), float(weights.max())
    norm = Normalize(w_min, w_max)
    cmap = matplotlib.colormaps["plasma"]

    for i in range(n_particles):
        ax.plot(
            temperatures,
            distances[:, i],
            color=cmap(norm(float(weights[i]))),
            alpha=0.25,
            linewidth=0.6,
        )

    ax.invert_xaxis()
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Distance from Focus")
    ax.set_title("Particle Phase Curves — Distance vs Temperature")

    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(sm, ax=ax, label="Particle Weight")

    return fig
