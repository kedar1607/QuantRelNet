"""Heat transfer utilities."""


def conduction_rate(k: float, area: float, d_temp: float, thickness: float) -> float:
    """Return heat transfer rate by conduction (Fourier's law)."""
    return k * area * d_temp / thickness


def radiation_rate(emissivity: float, area: float, temp: float) -> float:
    """Return radiation heat transfer rate via Stefan-Boltzmann law."""
    sigma = 5.670374419e-8
    return emissivity * sigma * area * temp**4
