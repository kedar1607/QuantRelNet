"""Ray tracing utilities."""

import numpy as np


def refract(incident: np.ndarray, normal: np.ndarray, n1: float, n2: float) -> np.ndarray:
    """Return refracted ray using Snell's law."""
    incident = incident / np.linalg.norm(incident)
    normal = normal / np.linalg.norm(normal)
    cos_i = -np.dot(normal, incident)
    sin_t2 = (n1 / n2) ** 2 * (1 - cos_i**2)
    if sin_t2 > 1:
        return np.zeros_like(incident)
    cos_t = (1 - sin_t2) ** 0.5
    return (n1 / n2) * incident + (cos_t - (n1 / n2) * cos_i) * normal
