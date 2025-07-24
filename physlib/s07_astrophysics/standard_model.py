"""Summary of particle masses in the Standard Model.

This file lists a small subset of elementary particles with their
rest masses in gigaelectronvolts (GeV).
"""

from dataclasses import dataclass


@dataclass
class Particle:
    name: str
    mass_GeV: float


# Example subset
PARTICLES = [
    Particle("electron", 0.000511),
    Particle("up quark", 0.0022),
    Particle("down quark", 0.0047),
]
