"""Utilities demonstrating conservation of momentum.

Linear momentum is defined as :math:`p = m v`.  For an isolated system
the total momentum remains constant.  These helpers illustrate basic
calculations and a two-body elastic collision in one dimension.
"""

from dataclasses import dataclass
import numpy as np


def momentum(mass: float, velocity: float) -> float:
    """Compute linear momentum :math:`p = m v`.

    Parameters
    ----------
    mass : float
        Mass of the object in kilograms.
    velocity : float
        Velocity in metres per second.
    """
    return mass * velocity


def momentum_vec(mass: float, velocity: np.ndarray) -> np.ndarray:
    """Return momentum vector for motion in 3D."""
    return mass * np.asarray(velocity)


@dataclass
class Collision:
    """Simple elastic collision in one dimension.

    Attributes
    ----------
    m1, m2 : float
        Masses of the two bodies.
    v1, v2 : float
        Initial velocities.
    """

    m1: float
    v1: float
    m2: float
    v2: float

    def final_velocities(self) -> tuple[float, float]:
        """Return final velocities for a perfectly elastic collision.

        The formulas come from conservation of momentum and kinetic
        energy under the assumption that no external forces act on the
        two-body system.
        """
        new_v1 = ((self.m1 - self.m2) / (self.m1 + self.m2)) * self.v1 + (
            (2 * self.m2) / (self.m1 + self.m2)
        ) * self.v2
        new_v2 = ((2 * self.m1) / (self.m1 + self.m2)) * self.v1 + (
            (self.m2 - self.m1) / (self.m1 + self.m2)
        ) * self.v2
        return new_v1, new_v2


@dataclass
class Collision3D:
    """Elastic collision for particles with velocity vectors.

    This simple extension applies the 1D formulas component-wise. It is
    accurate only when the collision is head-on along the velocity
    vectors but demonstrates momentum conservation in code.
    """

    m1: float
    v1: np.ndarray
    m2: float
    v2: np.ndarray

    def final_velocities(self) -> tuple[np.ndarray, np.ndarray]:
        coeff1 = (self.m1 - self.m2) / (self.m1 + self.m2)
        coeff2 = (2 * self.m2) / (self.m1 + self.m2)
        coeff3 = (2 * self.m1) / (self.m1 + self.m2)
        coeff4 = (self.m2 - self.m1) / (self.m1 + self.m2)
        new_v1 = coeff1 * self.v1 + coeff2 * self.v2
        new_v2 = coeff3 * self.v1 + coeff4 * self.v2
        return new_v1, new_v2
