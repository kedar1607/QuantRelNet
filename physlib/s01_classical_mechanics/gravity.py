"""Newtonian gravity calculations."""

G = 6.67430e-11


def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """Return gravitational force between two masses."""
    return G * m1 * m2 / distance**2


def orbital_velocity(mass_central: float, radius: float) -> float:
    """Return velocity required for a circular orbit."""
    return (G * mass_central / radius) ** 0.5
