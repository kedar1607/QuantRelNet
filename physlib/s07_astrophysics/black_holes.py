"""Black hole utilities.

Uses the Schwarzschild solution to compute the area of the event
horizon of a non-rotating (Schwarzschild) black hole.
"""

from ..s05_relativity.general import schwarzschild_radius


def event_horizon_area(mass: float) -> float:
    """Return event horizon surface area ``A = 4π r_s^2``."""
    r_s = schwarzschild_radius(mass)
    return 4 * 3.141592653589793 * r_s**2
