from dataclasses import dataclass

import numpy as np


@dataclass
class VelocimetryFrame:
    temperature: float
    distances: np.ndarray  # shape (N,) — one value per particle
