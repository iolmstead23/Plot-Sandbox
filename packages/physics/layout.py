"""Initial layout — heavier near focus, lighter on outer shell.

Maps each weight to a target distance from focus, then scatters at that
distance with a random angular direction (uniform on the unit sphere).
"""

import numpy as np


def initial_layout(
    weights: np.ndarray,
    *,
    view_range: float,
    rng: np.random.Generator,
    focus: np.ndarray | None = None,
    inner_radius_fraction: float = 0.1,
    outer_radius_fraction: float = 0.9,
) -> np.ndarray:
    n = weights.shape[0]
    if n == 0:
        return np.zeros((0, 3), dtype=np.float64)
    if focus is None:
        focus = np.zeros(3, dtype=np.float64)

    # Heaviest -> inner_radius_fraction*view_range, lightest -> outer_radius_fraction*view_range.
    w_min, w_max = float(weights.min()), float(weights.max())
    if w_max > w_min:
        normalized = (weights - w_min) / (w_max - w_min)
    else:
        normalized = np.full(n, 0.5)
    radius_scale = outer_radius_fraction - inner_radius_fraction
    radii = (outer_radius_fraction - radius_scale * normalized) * view_range

    # Marsaglia-style random unit directions on the sphere.
    u = rng.uniform(-1.0, 1.0, size=n)
    theta = rng.uniform(0.0, 2 * np.pi, size=n)
    sin_phi = np.sqrt(1.0 - u * u)
    dirs = np.stack(
        [sin_phi * np.cos(theta), sin_phi * np.sin(theta), u],
        axis=1,
    )

    return focus[None, :] + dirs * radii[:, None]
