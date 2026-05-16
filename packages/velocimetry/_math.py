import numpy as np


def distances_from_focus(positions: np.ndarray, focus: list[float]) -> np.ndarray:
    """Euclidean distance from each particle to the focus point. Shape: (N,)."""
    f = np.asarray(focus, dtype=float)
    return np.linalg.norm(positions - f[: positions.shape[1]], axis=1)
