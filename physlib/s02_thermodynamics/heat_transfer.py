"""Heat transfer utilities.

Two common mechanisms are included: conduction and thermal radiation.
Fourier's law for conduction states ``Q̇ = k A ΔT / L`` while the
Stefan–Boltzmann law for radiation is ``Q̇ = ε σ A T^4``.
"""


def conduction_rate(k: float, area: float, d_temp: float, thickness: float) -> float:
    """Return heat transfer rate by conduction ``Q̇``.

    Parameters
    ----------
    k : float
        Thermal conductivity.
    area : float
        Cross-sectional area ``A``.
    d_temp : float
        Temperature difference ``ΔT``.
    thickness : float
        Thickness ``L`` of the material.
    """
    return k * area * d_temp / thickness


def radiation_rate(emissivity: float, area: float, temp: float) -> float:
    """Return radiative heat transfer ``Q̇`` using Stefan–Boltzmann law."""
    sigma = 5.670374419e-8
    return emissivity * sigma * area * temp**4
