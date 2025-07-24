"""Entropy and statistical mechanics utilities."""

import math


def boltzmann_entropy(num_states: int) -> float:
    """Return Boltzmann entropy S = k_B * ln(W)."""
    k_B = 1.380649e-23
    return k_B * math.log(num_states)
