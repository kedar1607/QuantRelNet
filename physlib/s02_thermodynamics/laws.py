"""Laws of thermodynamics."""


def first_law(delta_u: float, heat: float) -> float:
    """Return work done from internal energy change and heat added."""
    return heat - delta_u


def efficiency(work: float, heat_in: float) -> float:
    """Return thermal efficiency."""
    return work / heat_in
