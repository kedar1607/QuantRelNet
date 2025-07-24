"""Entropy and statistical mechanics utilities.

The Boltzmann entropy formula relates the number of microstates ``W``
of a system to its entropy ``S`` through ``S = k_B \ln W`` where
``k_B`` is Boltzmann's constant.
"""

import math


def boltzmann_entropy(num_states: int) -> float:
    """Return Boltzmann entropy ``S = k_B \ln W``."""
    k_B = 1.380649e-23
    return k_B * math.log(num_states)
