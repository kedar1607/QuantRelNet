"""General relativity utilities."""


def schwarzschild_radius(mass: float) -> float:
    """Return Schwarzschild radius for a given mass."""
    G = 6.67430e-11
    c = 299_792_458.0
    return 2 * G * mass / c**2


def gravitational_time_dilation(mass: float, radius: float, proper_time: float) -> float:
    """Return gravitational time dilation near a massive body."""
    r_s = schwarzschild_radius(mass)
    return proper_time * (1 - r_s / radius) ** 0.5
