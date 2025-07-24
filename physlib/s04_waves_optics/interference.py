"""Interference and diffraction utilities."""

import numpy as np


def double_slit_intensity(a: float, d: float, wavelength: float, screen_dist: float, x: np.ndarray) -> np.ndarray:
    """Return intensity pattern for double-slit experiment."""
    beta = (np.pi * a * x) / (wavelength * screen_dist)
    gamma = (np.pi * d * x) / (wavelength * screen_dist)
    return (np.sin(beta) / beta) ** 2 * (np.cos(gamma)) ** 2
