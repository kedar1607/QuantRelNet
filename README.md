# QuantRelNet 🌌⚛️

A comprehensive Python library for exploring and visualizing fundamental physics concepts from classical mechanics to astrophysics.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

**QuantRelNet** provides both computational tools and stunning visualizations across all major physics domains:

- 🎯 **Physics Calculations**: Lightweight utilities for key physics formulas and concepts
- 🎬 **Interactive Animations**: Real-time simulations of physical phenomena
- 🎮 **Interactive Controls**: Sliders and buttons to explore parameter spaces
- 📊 **Educational Visualizations**: Clear, publication-quality plots and diagrams
- 🔗 **Cross-Domain Integration**: Functions that connect different areas of physics

## 📚 Physics Coverage

```
physlib/
├── s01_classical_mechanics/     # Newton's laws, collisions, orbits
├── s02_thermodynamics/         # Heat engines, entropy, gas dynamics
├── s03_electromagnetism/       # Fields, waves, particle motion
├── s04_waves_optics/          # Interference, diffraction, ray tracing
├── s05_relativity/           # Special & general relativity effects
├── s06_quantum_mechanics/    # Wave functions, tunneling, uncertainty
└── s07_astrophysics/        # Cosmic expansion, black holes, stellar evolution
```

Each module contains both **computational utilities** and **interactive visualizations**.

## 🛠️ Installation

### Basic Installation
```bash
git clone https://github.com/your-username/QuantRelNet.git
cd QuantRelNet
pip install -e .
```

### With Visualization Support
```bash
pip install -e .[visualization]
```

### Development Installation
```bash
pip install -e .[dev]
```

### Requirements
- Python 3.9+
- NumPy 1.24+
- Matplotlib 3.7+ (for visualizations)
- SciPy 1.10+ (for advanced calculations)

## 🎮 Quick Start

### Basic Physics Calculations

```python
import numpy as np
from physlib.s01_classical_mechanics import newton, energy
from physlib.s06_quantum_mechanics import uncertainty

# Classical mechanics
force = newton.force(mass=2.0, acceleration=9.81)
ke = energy.kinetic_energy(mass=1.0, velocity=10.0)

# Quantum mechanics
is_valid = uncertainty.verify_uncertainty(delta_x=1e-10, delta_p=6e-25)
```

### Interactive Visualizations

```python
# Run individual demonstrations
from physlib.s01_classical_mechanics.visualizations import demo_pendulum
from physlib.s06_quantum_mechanics.visualizations import demo_wave_packet

demo_pendulum()        # Animated pendulum simulation
demo_wave_packet()     # Quantum wave packet evolution
```

### Comprehensive Showcase

```python
# Interactive menu system
python examples/visualization_showcase.py

# Quick tour of key concepts
python examples/visualization_showcase.py --quick

# Physics concept comparisons
python examples/visualization_showcase.py --compare
```

## 🎨 Visualization Examples

### Classical Mechanics
- **Projectile Motion**: Parabolic trajectories with air resistance
- **Pendulum Dynamics**: Simple and damped oscillations
- **Particle Collisions**: Elastic and inelastic collision dynamics
- **Orbital Mechanics**: Gravitational orbits and Kepler's laws
- **Spring-Mass Systems**: Harmonic motion with customizable parameters

### Quantum Mechanics
- **Wave Packet Evolution**: Gaussian wave packets with dispersion
- **Quantum Tunneling**: Barrier penetration visualization
- **Uncertainty Principle**: Position-momentum trade-offs
- **Harmonic Oscillator**: Energy eigenstates and time evolution
- **Measurement Collapse**: State reduction visualization

### Electromagnetism
- **Electric Field Lines**: Point charges, dipoles, and configurations
- **Magnetic Field Visualization**: Current loops and solenoids
- **Charged Particle Motion**: Lorentz force trajectories
- **Electromagnetic Waves**: 2D and 3D wave propagation
- **Field Superposition**: Multiple source interactions

### Relativity
- **Spacetime Diagrams**: Minkowski diagrams with world lines
- **Time Dilation**: Clock synchronization effects
- **Length Contraction**: Lorentz transformation visualization
- **Twin Paradox**: Age difference calculations
- **Black Hole Physics**: Event horizons and gravitational effects

### Astrophysics
- **Cosmic Expansion**: Hubble's law and galaxy recession
- **Black Hole Accretion**: Matter spiraling into event horizons
- **Stellar Evolution**: HR diagrams and lifecycle paths
- **Gravitational Lensing**: Light bending around massive objects
- **Galaxy Collisions**: N-body dynamics and tidal effects

## 🎯 Example Demonstrations

### Quantum Wave Packet Animation
```python
from physlib.s06_quantum_mechanics.visualizations import QuantumWavePacket

# Create animated quantum wave packet
sim = QuantumWavePacket(initial_position=-3.0, initial_momentum=2.0, sigma=0.5)
sim.start_animation(interval=50, frames=400)
sim.show()
```

### Interactive Orbital Mechanics
```python
from physlib.s01_classical_mechanics.visualizations import create_orbital_motion_demo

# Interactive orbital simulation with parameter controls
orbital_demo = create_orbital_motion_demo()
orbital_demo.show()  # Includes sliders for mass, distance, velocity
```

### Electromagnetic Field Visualization
```python
from physlib.s03_electromagnetism.visualizations import ElectricFieldVisualization

# Multiple charge configurations
field_viz = ElectricFieldVisualization()
field_viz.show()  # Shows point charges, dipoles, parallel plates
```

## 🔬 Advanced Features

### Custom Physics Simulations
```python
from physlib.visualization import PhysicsAnimation, ParticleTracker

class CustomSimulation(PhysicsAnimation):
    def __init__(self):
        super().__init__(figsize=(10, 8))
        # Your custom physics here
        
    def animate(self, frame):
        # Update physics each frame
        return self.plot_elements
```

### Interactive Parameter Control
```python
from physlib.visualization import InteractivePhysicsPlot

plot = InteractivePhysicsPlot()
plot.add_slider('Mass', 0.1, 10.0, 1.0, callback_function)
plot.add_button('Reset', reset_function)
plot.show()
```

### Multi-Physics Integration
```python
# Combine concepts from different domains
from physlib.s01_classical_mechanics import gravity
from physlib.s05_relativity import special

# Classical gravity
F_classical = gravity.gravitational_force(m1, m2, r)

# Relativistic time dilation
gamma = special.lorentz_factor(velocity)
```

## 📖 Educational Use

QuantRelNet is designed for:

- **Physics Students**: Visual learning of abstract concepts
- **Educators**: Interactive classroom demonstrations
- **Researchers**: Quick prototyping of physics simulations
- **Science Communicators**: Engaging physics visualizations
- **Self-Learners**: Hands-on exploration of physics principles

### Key Educational Features

- 📝 **Detailed Docstrings**: Every function explains the underlying physics
- 🔗 **External References**: Links to Wikipedia and physics resources
- 🎛️ **Parameter Exploration**: Interactive controls for concept understanding
- 🎨 **Visual Clarity**: Clean, publication-quality visualizations
- 🔄 **Progressive Complexity**: From simple concepts to advanced phenomena

## 🧪 Example Gallery

### Run All Demonstrations
```bash
# Interactive menu system
python examples/visualization_showcase.py

# Quick tour (one demo per physics area)
python examples/visualization_showcase.py --quick

# Side-by-side concept comparisons
python examples/visualization_showcase.py --compare

# Custom multi-physics demonstration
python examples/visualization_showcase.py --custom
```

### Individual Topic Demos
```python
# Classical mechanics
from physlib.s01_classical_mechanics.visualizations import *
demo_projectile()  # Projectile with air resistance
demo_collision()   # Elastic/inelastic collisions

# Quantum mechanics  
from physlib.s06_quantum_mechanics.visualizations import *
demo_tunneling()              # Barrier penetration
demo_uncertainty_principle()  # Heisenberg uncertainty

# Astrophysics
from physlib.s07_astrophysics.visualizations import *
demo_cosmic_expansion()    # Hubble's law
demo_black_hole_accretion() # Matter falling into black holes
```

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- 🐛 **Bug Reports**: Found an issue? Let us know!
- 🎯 **New Physics**: Add visualizations for additional concepts
- 🎨 **Improved Graphics**: Better visualizations and animations
- 📚 **Documentation**: Examples, tutorials, and explanations
- 🧪 **Testing**: Unit tests and validation

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Physics concepts from standard textbooks and research papers
- Visualization inspiration from physics education literature
- Community feedback and contributions

## 🔗 Links

- 📖 [Documentation](https://your-docs-link.com)
- 🐛 [Issue Tracker](https://github.com/your-username/QuantRelNet/issues)
- 💬 [Discussions](https://github.com/your-username/QuantRelNet/discussions)

---

**Explore the universe through code!** 🌌 From quantum mechanics to cosmic expansion, QuantRelNet makes physics interactive, visual, and accessible.
