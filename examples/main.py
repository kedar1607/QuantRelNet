"""Example script demonstrating library usage."""

import numpy as np
from physlib.s01_classical_mechanics import newton, energy, momentum, gravity
from physlib.s02_thermodynamics import laws, heat_transfer
from physlib.s03_electromagnetism import lorentz
from physlib.s04_waves_optics import wave_equation
from physlib.s05_relativity import special
from physlib.s06_quantum_mechanics import uncertainty


# Classical mechanics
acc = newton.acceleration(force=10, mass=2)
print("Acceleration:", acc)
print("Kinetic energy:", energy.kinetic_energy(2, 3))

# Thermodynamics
print("Work from first law:", laws.first_law(delta_u=5, heat=10))
print("Conduction rate:", heat_transfer.conduction_rate(1, 2, 10, 0.1))

# Electromagnetism
F = lorentz.lorentz_force(1.6e-19, np.array([1, 0, 0]), np.array([0, 0, 1]), np.array([0, 1e6, 0]))
print("Lorentz force:", F)

# Waves
x = np.linspace(0, 1, 5)
print("Wave sample:", wave_equation.wave_solution(1, 2*np.pi, 2*np.pi, x, t=0.5))

# Relativity
print("Time dilation:", special.time_dilation(1, 100000))

# Quantum mechanics
print("Heisenberg satisfied:", uncertainty.verify_uncertainty(1e-10, 6e-25))
