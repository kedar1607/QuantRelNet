"""Newtonian gravity calculations.

The law of universal gravitation states

.. math:: F = G \frac{m_1 m_2}{r^2},

where ``G`` is the gravitational constant (``6.67430e-11`` in SI units),
``m_1`` and ``m_2`` are masses and ``r`` is the separation.
"""

G = 6.67430e-11

import numpy as np


def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """Return gravitational force ``F`` between ``m1`` and ``m2``.

    Parameters
    ----------
    m1, m2 : float
        Masses in kilograms.
    distance : float
        Separation ``r`` in metres.
    """
    return G * m1 * m2 / distance**2


def gravitational_force_vector(m1: float, m2: float, r_vec: np.ndarray) -> np.ndarray:
    """Return gravitational force vector between ``m1`` and ``m2`` separated by ``r_vec``."""
    r = np.asarray(r_vec)
    r_mag = np.linalg.norm(r)
    return -G * m1 * m2 * r / r_mag**3


def orbital_velocity(mass_central: float, radius: float) -> float:
    """Velocity required for a circular orbit of radius ``radius``.

    Derived by setting the gravitational force equal to the centripetal
    force :math:`m v^2 / r`.  ``mass_central`` is the central mass.
    """
    return (G * mass_central / radius) ** 0.5
