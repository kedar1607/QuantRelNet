"""Maxwell's equations utilities."""

import numpy as np


class MaxwellSolver:
    """Very simplified finite difference solver for wave equation."""

    def __init__(self, c: float = 299_792_458.0):
        self.c = c

    def step(self, e_field: np.ndarray, b_field: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
        """Advance electromagnetic fields by one time step.

        This naive implementation demonstrates field propagation using
        curl relations from Maxwell's equations. It is not stable for
        real simulations but illustrates code structure.
        """
        curl_e = np.gradient(e_field)[0]
        curl_b = np.gradient(b_field)[0]
        new_e = e_field + self.c**2 * curl_b * dt
        new_b = b_field - curl_e * dt
        return new_e, new_b
