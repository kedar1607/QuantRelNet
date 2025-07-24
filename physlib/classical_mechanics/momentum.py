"""Conservation of momentum utilities."""

from dataclasses import dataclass


def momentum(mass: float, velocity: float) -> float:
    """Return momentum p = mv."""
    return mass * velocity


@dataclass
class Collision:
    """Simple elastic collision in one dimension."""

    m1: float
    v1: float
    m2: float
    v2: float

    def final_velocities(self) -> tuple[float, float]:
        """Return final velocities for an elastic collision."""
        new_v1 = ((self.m1 - self.m2) / (self.m1 + self.m2)) * self.v1 + (
            (2 * self.m2) / (self.m1 + self.m2)
        ) * self.v2
        new_v2 = ((2 * self.m1) / (self.m1 + self.m2)) * self.v1 + (
            (self.m2 - self.m1) / (self.m1 + self.m2)
        ) * self.v2
        return new_v1, new_v2
