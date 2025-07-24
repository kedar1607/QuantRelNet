"""Utilities for Newton's laws of motion.

Each function documents the corresponding physical law.  Newton's
Second Law states that the net force :math:`F` on an object is equal
to the product of its mass :math:`m` and acceleration :math:`a`
(`F = m a`).  Throughout this module ``mass`` is measured in kilograms,
``force`` in newtons and ``acceleration`` in metres per second squared.

See https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion for a short
overview.
"""

from dataclasses import dataclass


def acceleration(force: float, mass: float) -> float:
    """Compute acceleration :math:`a = F/m`.

    Parameters
    ----------
    force : float
        Net force :math:`F` in newtons.
    mass : float
        Object mass :math:`m` in kilograms.

    Returns
    -------
    float
        Acceleration in metres per second squared.
    """
    return force / mass


def force(mass: float, acceleration: float) -> float:
    """Compute force :math:`F = m a`.

    Parameters
    ----------
    mass : float
        Object mass in kilograms.
    acceleration : float
        Desired acceleration in metres per second squared.

    Returns
    -------
    float
        Force in newtons.
    """
    return mass * acceleration


@dataclass
class Particle:
    """A simple particle with mass and velocity.

    Parameters
    ----------
    mass : float
        Mass :math:`m` of the particle in kilograms.
    velocity : float
        Initial velocity :math:`v` in metres per second.
    """

    mass: float
    velocity: float

    def apply_force(self, force: float, time: float) -> None:
        """Update velocity after a constant force acts for ``time`` seconds.

        The velocity increment ``Δv`` is obtained from
        :math:`F = m a` and :math:`a = Δv / Δt`, giving
        :math:`Δv = (F/m) Δt`.
        """
        self.velocity += acceleration(force, self.mass) * time
