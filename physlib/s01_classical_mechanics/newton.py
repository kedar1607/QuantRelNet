"""Utilities for Newton's laws of motion."""

from dataclasses import dataclass


def acceleration(force: float, mass: float) -> float:
    """Return acceleration from force and mass using a = F/m."""
    return force / mass


def force(mass: float, acceleration: float) -> float:
    """Return force using F = ma."""
    return mass * acceleration


@dataclass
class Particle:
    """A simple particle with mass and velocity."""

    mass: float
    velocity: float

    def apply_force(self, force: float, time: float) -> None:
        """Update velocity after applying a constant force for a time interval."""
        self.velocity += acceleration(force, self.mass) * time
