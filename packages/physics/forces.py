"""Pure NumPy force functions. Each returns an (N, 3) net-force-per-node array.

No imports from other packages. The DOM is never referenced — these are plain
math on arrays. The orchestrator (handlers/tick.py) reads DOM arrays, passes
them in, and writes the integrator output back.
"""

import numpy as np


def central_gravity(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_g: float,
    focus: np.ndarray,
) -> np.ndarray:
    # Linear pull toward focus, scaled by mass. Heavier nodes feel a stronger
    # tug, so they settle nearer the center. Linear (not 1/r^2) is the stable
    # choice for force-directed layouts.
    return -k_g * weights[:, None] * (positions - focus[None, :])


def pairwise_repulsion(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_r: float,
    soft_core_radius: float,
) -> np.ndarray:
    n = positions.shape[0]
    if n < 2:
        return np.zeros_like(positions)

    diff = positions[:, None, :] - positions[None, :, :]   # i - j, shape (N, N, 3)
    d = np.linalg.norm(diff, axis=-1)
    d_safe = np.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]                   # unit vectors away from j

    # Soft core: linear ramp under r0, inverse-square above. No singularity.
    inv_sq = 1.0 / (d_safe * d_safe)
    soft = np.clip((soft_core_radius - d) / soft_core_radius, 0.0, 1.0)
    near = d < soft_core_radius
    mag = np.where(near, soft, inv_sq)
    np.fill_diagonal(mag, 0.0)

    mass_pair = weights[:, None] * weights[None, :]
    forces = (k_r * mag * mass_pair)[..., None] * direction   # (N, N, 3)
    return forces.sum(axis=1)


def pairwise_attraction(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_a: float,
    soft_core_radius: float,
) -> np.ndarray:
    n = positions.shape[0]
    if n < 2:
        return np.zeros_like(positions)

    diff = positions[None, :, :] - positions[:, None, :]   # j - i, toward j
    d = np.linalg.norm(diff, axis=-1)
    d_safe = np.where(d > 0.0, d, 1.0)
    direction = diff / d_safe[..., None]

    # Soft core flattens magnitude under r0 to 1/r0^2 so close pairs don't
    # gain unbounded pull and fight the repulsion forever.
    flat_mag = 1.0 / (soft_core_radius * soft_core_radius)
    inv_sq = 1.0 / (d_safe * d_safe)
    near = d < soft_core_radius
    mag = np.where(near, flat_mag, inv_sq)
    np.fill_diagonal(mag, 0.0)

    mass_pair = weights[:, None] * weights[None, :]
    forces = (k_a * mag * mass_pair)[..., None] * direction
    return forces.sum(axis=1)
