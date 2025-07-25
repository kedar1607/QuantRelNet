"""Utilities for the Schrödinger equation.

Provides a minimal finite-difference solver for the 1D time-dependent
Schrödinger equation

.. math:: i \hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi + V(x)\psi.

This example is purely educational and not meant for serious
simulations.
"""

import numpy as np
from typing import Callable


class Schrodinger1D:
    """Solve the time-dependent Schrödinger equation in 1D.

    The scheme uses a simple explicit method and is unstable for large
    time steps.  ``potential`` should return ``V(x)`` for an array ``x``.
    """

    def __init__(self, potential: Callable[[np.ndarray], np.ndarray], dx: float, dt: float):
        self.potential = potential
        self.dx = dx
        self.dt = dt
        self.hbar = 1.054_571_817e-34
        self.m = 9.109_383_7015e-31  # electron mass

    def step(self, psi: np.ndarray) -> np.ndarray:
        """Advance wave function ``psi`` by one time step ``dt``."""
        laplacian = (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / self.dx**2
        potential_term = self.potential(np.arange(len(psi)) * self.dx) * psi
        return psi + 1j * self.dt / (2 * self.hbar / self.m) * (laplacian - potential_term)


class Schrodinger3D:
    """Very small 3D Schrödinger solver using finite differences."""

    def __init__(self, potential: Callable[[tuple[int, int, int]], np.ndarray], dx: float, dt: float):
        self.potential = potential
        self.dx = dx
        self.dt = dt
        self.hbar = 1.054_571_817e-34
        self.m = 9.109_383_7015e-31

    def step(self, psi: np.ndarray) -> np.ndarray:
        laplacian = (
            np.roll(psi, -1, 0) + np.roll(psi, 1, 0)
            + np.roll(psi, -1, 1) + np.roll(psi, 1, 1)
            + np.roll(psi, -1, 2) + np.roll(psi, 1, 2) - 6 * psi
        ) / self.dx**2
        potential_term = self.potential(psi.shape) * psi
        return psi + 1j * self.dt / (2 * self.hbar / self.m) * (laplacian - potential_term)
