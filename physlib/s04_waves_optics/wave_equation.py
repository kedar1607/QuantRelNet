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


def wave_solution_3d(amplitude: float, k_vec: np.ndarray, omega: float, position: np.ndarray, t: float) -> np.ndarray:
    """Return sinusoidal wave ``A sin(k·x - ωt)`` for 3D ``position``."""
    k_vec = np.asarray(k_vec)
    pos = np.asarray(position)
    phase = np.dot(pos, k_vec)
    return amplitude * np.sin(phase - omega * t)
