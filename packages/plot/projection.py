"""Projects an (N, D) position array down to (N, 3) via PCA for rendering."""

import numpy as np


def project_to_3d(positions: np.ndarray) -> np.ndarray:
    """Returns (N, 3). If D <= 3, pads with zeros. If D > 3, takes top-3 principal components."""
    _, d = positions.shape
    if d == 3:
        return positions
    if d < 3:
        return np.pad(positions, ((0, 0), (0, 3 - d)))
    centered = positions - positions.mean(axis=0)
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    return centered @ Vt[:3].T
