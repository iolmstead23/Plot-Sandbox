"""Initial layout — radial shell placement with configurable weight-to-radius ordering.

layout_noise controls whether particles are placed in weight-sorted shells or
shuffled across shells:

  0.0 — deterministic: heavy particles at inner_radius, light at outer_radius.
         Initial Pearson r(weight, distance) = -1.0. The physics has nothing to
         discover; useful for rendering benchmarks and UI development.

  1.0 — weight-shuffled: the same shell radii are computed but randomly assigned
         to particles regardless of weight. r₀ ≈ 0. The forces must drive
         stratification from scratch, which is what the velocimetry study measures.

  (0, 1) — linear blend of the sorted and shuffled radius arrays. Particles start
            partially out of their equilibrium shells. Variance of initial radii
            is reduced relative to either extreme.
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
    layout_noise: float = 1.0,
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

    # Sorted radii: heaviest → inner_radius_fraction*view_range,
    #               lightest  → outer_radius_fraction*view_range.
    w_min, w_max = float(weights.min()), float(weights.max())
    if w_max > w_min:
        normalized = (weights - w_min) / (w_max - w_min)
    else:
        normalized = np.full(n, 0.5)
    radius_scale = outer_radius_fraction - inner_radius_fraction
    radii = (outer_radius_fraction - radius_scale * normalized) * view_range

    # Apply layout_noise: shuffle or blend the radius assignments.
    noise = float(np.clip(layout_noise, 0.0, 1.0))
    if noise >= 1.0:
        rng.shuffle(radii)
    elif noise > 0.0:
        shuffled = radii.copy()
        rng.shuffle(shuffled)
        radii = (1.0 - noise) * radii + noise * shuffled

    # Gaussian-normalized unit vectors are uniformly distributed on the (D-1)-sphere.
    raw = rng.standard_normal((n, dims))
    norms = np.linalg.norm(raw, axis=1, keepdims=True)
    norms = np.where(norms > 0.0, norms, 1.0)
    dirs = raw / norms

    return focus_d[None, :] + dirs * radii[:, None]
