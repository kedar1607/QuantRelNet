"""Black hole utilities."""

from ..s05_relativity.general import schwarzschild_radius


def event_horizon_area(mass: float) -> float:
    """Return event horizon area for a non-spinning black hole."""
    r_s = schwarzschild_radius(mass)
    return 4 * 3.141592653589793 * r_s**2
