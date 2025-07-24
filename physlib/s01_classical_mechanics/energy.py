"""Energy calculations using Newtonian mechanics."""

from .newton import force


def kinetic_energy(mass: float, velocity: float) -> float:
    """Return kinetic energy, KE = 0.5 * m * v^2."""
    return 0.5 * mass * velocity ** 2


def potential_energy(mass: float, height: float, g: float = 9.81) -> float:
    """Return gravitational potential energy, PE = mgh."""
    return mass * g * height


def work_done(mass: float, acceleration_val: float, distance: float) -> float:
    """Compute work done using Newton's second law and distance.

    This demonstrates calling another module: we use ``force`` from
    ``newton`` because work = F * d and F = ma.
    """
    f = force(mass, acceleration_val)
    return f * distance
