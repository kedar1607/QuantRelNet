"""Selected laws of thermodynamics.

The *First Law* relates heat ``Q``, work ``W`` and internal energy
change ``\Delta U`` via ``\Delta U = Q - W``.  The ``efficiency`` helper
implements the definition of thermal efficiency ``\eta = W/Q_{in}``.
"""


def first_law(delta_u: float, heat: float) -> float:
    """Compute work ``W`` from the First Law ``\Delta U = Q - W``."""
    return heat - delta_u


def efficiency(work: float, heat_in: float) -> float:
    """Return thermal efficiency ``\eta = W/ Q_{in}``."""
    return work / heat_in
