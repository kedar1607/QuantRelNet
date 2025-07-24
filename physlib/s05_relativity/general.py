"""General relativity utilities.

Uses the Schwarzschild solution of Einstein's field equations to
demonstrate gravitational effects such as the event horizon radius and
time dilation near a massive body.
"""


def schwarzschild_radius(mass: float) -> float:
    """Return Schwarzschild radius ``r_s = 2 G M / c^2``."""
    G = 6.67430e-11
    c = 299_792_458.0
    return 2 * G * mass / c**2


def gravitational_time_dilation(mass: float, radius: float, proper_time: float) -> float:
    """Return gravitational time dilation ``t = τ \sqrt{1 - r_s/r}``."""
    r_s = schwarzschild_radius(mass)
    return proper_time * (1 - r_s / radius) ** 0.5
