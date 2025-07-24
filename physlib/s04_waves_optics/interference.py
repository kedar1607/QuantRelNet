"""Interference and diffraction utilities.

Implements the Fraunhofer diffraction pattern for a double-slit
experiment.  The resulting intensity is

.. math:: I(x) = \left(\frac{\sin \beta}{\beta}\right)^2 \cos^2 \gamma

with ``β = π a x/(λ L)`` and ``γ = π d x/(λ L)``. Here ``a`` is slit
width, ``d`` the slit separation, ``λ`` the wavelength and ``L`` the
distance to the screen.
"""

import numpy as np


def double_slit_intensity(a: float, d: float, wavelength: float, screen_dist: float, x: np.ndarray) -> np.ndarray:
    """Return intensity pattern ``I(x)`` for the double-slit experiment."""
    beta = (np.pi * a * x) / (wavelength * screen_dist)
    gamma = (np.pi * d * x) / (wavelength * screen_dist)
    return (np.sin(beta) / beta) ** 2 * (np.cos(gamma)) ** 2
