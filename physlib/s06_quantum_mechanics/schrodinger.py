"""Utilities for the Schrödinger equation."""

import numpy as np
from typing import Callable


class Schrodinger1D:
    """Solve the time-dependent Schrödinger equation in 1D.

    This is a very small explicit finite difference demonstration and not
    suitable for production use.
    """

    def __init__(self, potential: Callable[[np.ndarray], np.ndarray], dx: float, dt: float):
        self.potential = potential
        self.dx = dx
        self.dt = dt
        self.hbar = 1.054_571_817e-34
        self.m = 9.109_383_7015e-31  # electron mass

    def step(self, psi: np.ndarray) -> np.ndarray:
        """Advance wave function by one time step."""
        laplacian = (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / self.dx**2
        potential_term = self.potential(np.arange(len(psi)) * self.dx) * psi
        return psi + 1j * self.dt / (2 * self.hbar / self.m) * (laplacian - potential_term)
