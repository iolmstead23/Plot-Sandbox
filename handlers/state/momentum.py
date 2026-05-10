import numpy as np

from packages.config import config

_prev: np.ndarray | None = None


def reset() -> None:
    global _prev
    _prev = None


def smooth(proposed: np.ndarray) -> np.ndarray:
    global _prev
    damping = config.physics.damping
    if _prev is not None and _prev.shape == proposed.shape and damping > 0.0:
        result = (1.0 - damping) * proposed + damping * _prev
    else:
        result = proposed
    _prev = result
    return result
