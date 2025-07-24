"""Utilities demonstrating conservation of momentum.

Linear momentum is defined as :math:`p = m v`.  For an isolated system
the total momentum remains constant.  These helpers illustrate basic
calculations and a two-body elastic collision in one dimension.
"""

from dataclasses import dataclass


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
