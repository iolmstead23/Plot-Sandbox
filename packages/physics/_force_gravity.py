import numpy as np

from ._backend import get_module


def central_gravity(
    positions: np.ndarray,
    weights: np.ndarray,
    *,
    k_g: float,
    focus: np.ndarray,
    soft_core_radius: float,
) -> np.ndarray:
    xp = get_module(positions)
    focus = xp.asarray(focus)
    # Constant-magnitude inward force, scaled by mass. The soft-core denominator
    # blends to a linear restoring force inside the core radius so nodes that
    # cross the focus do not oscillate indefinitely.
    delta = positions - focus[None, :]
    r_sq = xp.sum(delta * delta, axis=-1, keepdims=True)
    r_soft = xp.sqrt(r_sq + soft_core_radius * soft_core_radius)
    return -k_g * weights[:, None] * (delta / r_soft)
