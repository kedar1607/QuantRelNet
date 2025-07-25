"""Energy calculations using Newtonian mechanics.

This module provides basic formulas for mechanical energy.  The
definitions stem from the work-energy theorem and the conservation of
energy.  Units are SI: kilograms, metres and seconds.
"""

import numpy as np
from .newton import force, force_vec


def kinetic_energy(mass: float, velocity: float) -> float:
    """Compute kinetic energy :math:`K = \tfrac{1}{2} m v^2`.

    Parameters
    ----------
    mass : float
        Mass :math:`m` in kilograms.
    velocity : float
        Speed :math:`v` in metres per second.
    """
    return 0.5 * mass * velocity ** 2


def kinetic_energy_vec(mass: float, velocity: np.ndarray) -> float:
    """Return kinetic energy for a velocity vector."""
    speed = np.linalg.norm(velocity)
    return 0.5 * mass * speed**2


def potential_energy(mass: float, height: float, g: float = 9.81) -> float:
    """Compute gravitational potential energy :math:`U = m g h`.

    ``g`` defaults to Earth's surface gravity (:math:`9.81\,\text{m/s}^2`).
    """
    return mass * g * height


def work_done(mass: float, acceleration_val: float, distance: float) -> float:
    """Compute work :math:`W = F d` from Newton's second law.

    Parameters
    ----------
    mass : float
        Mass of the object.
    acceleration_val : float
        Constant acceleration.
    distance : float
        Distance :math:`d` over which the force acts.

    Notes
    -----
    ``force`` from :mod:`newton` is used to demonstrate inter-module
    calls, since :math:`F = m a` relates the parameters.
    """
    f = force(mass, acceleration_val)
    return f * distance


def work_done_vec(mass: float, acceleration_vec: np.ndarray, displacement: np.ndarray) -> float:
    """Return work from vector force and displacement."""
    f_vec = force_vec(mass, acceleration_vec)
    return float(np.dot(f_vec, displacement))
