"""Wave equation utilities.

Provides a simple sinusoidal solution to the one-dimensional wave
equation:

.. math:: y(x,t) = A \sin(k x - \omega t)

where ``A`` is amplitude, ``k`` the wave number and ``ω`` the angular
frequency.
"""

import numpy as np


def wave_solution(amplitude: float, k: float, omega: float, x: np.ndarray, t: float) -> np.ndarray:
    """Return the value of ``y(x,t)`` for a sinusoidal travelling wave."""
    return amplitude * np.sin(k * x - omega * t)
