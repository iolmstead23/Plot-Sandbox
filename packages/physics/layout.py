"""Initial layout — heavier near focus, lighter on outer shell.

Maps each weight to a target distance from focus, then scatters at that
distance with a random unit direction in N-D space.
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
    dims: int = 3,
) -> np.ndarray:
    n = weights.shape[0]
    if n == 0:
        return np.zeros((0, dims), dtype=np.float64)

    if focus is None:
        focus_d = np.zeros(dims, dtype=np.float64)
    else:
        focus = np.asarray(focus, dtype=np.float64).reshape(-1)
        focus_d = np.zeros(dims, dtype=np.float64)
        copy_n = min(focus.shape[0], dims)
        focus_d[:copy_n] = focus[:copy_n]

    # Heaviest -> inner_radius_fraction*view_range, lightest -> outer_radius_fraction*view_range.
    w_min, w_max = float(weights.min()), float(weights.max())
    if w_max > w_min:
        normalized = (weights - w_min) / (w_max - w_min)
    else:
        normalized = np.full(n, 0.5)
    radius_scale = outer_radius_fraction - inner_radius_fraction
    radii = (outer_radius_fraction - radius_scale * normalized) * view_range

    # Gaussian-normalized unit vectors are uniformly distributed on the (D-1)-sphere.
    raw = rng.standard_normal((n, dims))
    norms = np.linalg.norm(raw, axis=1, keepdims=True)
    norms = np.where(norms > 0.0, norms, 1.0)
    dirs = raw / norms

    return focus_d[None, :] + dirs * radii[:, None]
