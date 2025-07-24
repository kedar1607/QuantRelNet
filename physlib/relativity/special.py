"""Special relativity utilities."""

import numpy as np

c = 299_792_458.0


def time_dilation(proper_time: float, velocity: float) -> float:
    """Return dilated time from proper time and velocity."""
    gamma = 1 / np.sqrt(1 - (velocity / c) ** 2)
    return gamma * proper_time


def length_contraction(proper_length: float, velocity: float) -> float:
    """Return contracted length from proper length and velocity."""
    gamma = 1 / np.sqrt(1 - (velocity / c) ** 2)
    return proper_length / gamma
