"""Wave equation utilities."""

import numpy as np


def wave_solution(amplitude: float, k: float, omega: float, x: np.ndarray, t: float) -> np.ndarray:
    """Return sinusoidal wave solution."""
    return amplitude * np.sin(k * x - omega * t)
