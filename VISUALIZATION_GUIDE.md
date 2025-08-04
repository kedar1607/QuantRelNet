# QuantRelNet Visualization Guide 🎨

A comprehensive guide to the physics visualizations and animations available in QuantRelNet.

## 🚀 Quick Start

### Run Interactive Showcase
```bash
# Interactive menu with all demonstrations
python examples/visualization_showcase.py

# Quick tour of key concepts
python examples/visualization_showcase.py --quick

# Compare concepts across physics domains
python examples/visualization_showcase.py --compare
```

### Install Visualization Dependencies
```bash
pip install -e .[visualization]  # Core visualization support
pip install -e .[dev]           # Full development environment
```

## 📚 Physics Domains

## 1. Classical Mechanics 🎯

### Available Visualizations

#### Projectile Motion
```python
from physlib.s01_classical_mechanics.visualizations import ProjectileMotion, demo_projectile

# Basic demo
demo_projectile()

# Custom simulation
sim = ProjectileMotion(v0=25, angle=45, drag_coeff=0.1)
sim.start_animation(interval=30, frames=300)
sim.show()
```
**Features**: Air resistance, trajectory tracking, velocity vectors

#### Pendulum Dynamics
```python
from physlib.s01_classical_mechanics.visualizations import PendulumSimulation, demo_pendulum

# Damped pendulum
sim = PendulumSimulation(length=2.0, theta0=60, damping=0.05)
sim.start_animation()
sim.show()
```
**Features**: Damping effects, energy visualization, trail tracking

#### Spring-Mass Systems
```python
from physlib.s01_classical_mechanics.visualizations import SpringMassSystem

sim = SpringMassSystem(mass=2.0, k=10.0, damping=0.3)
sim.start_animation()
sim.show()
```
**Features**: Position vs time plots, phase space, resonance

#### Particle Collisions
```python
from physlib.s01_classical_mechanics.visualizations import CollisionSimulation

# Elastic collision
sim = CollisionSimulation(m1=1.0, m2=2.0, v1=5.0, v2=-1.0, restitution=1.0)
sim.start_animation()
sim.show()
```
**Features**: Conservation laws, momentum analysis, restitution effects

#### Interactive Orbital Mechanics
```python
from physlib.s01_classical_mechanics.visualizations import create_orbital_motion_demo

demo = create_orbital_motion_demo()
demo.show()  # Interactive sliders for parameters
```
**Features**: Kepler's laws, orbital shapes, gravitational forces

---

## 2. Thermodynamics 🌡️

### Available Visualizations

#### Kinetic Theory of Gases
```python
from physlib.s02_thermodynamics.visualizations import GasParticleSimulation, demo_gas_particles

sim = GasParticleSimulation(n_particles=200, temperature=400)
sim.start_animation()
sim.show()
```
**Features**: Maxwell-Boltzmann distribution, temperature effects, particle tracking

#### Heat Diffusion
```python
from physlib.s02_thermodynamics.visualizations import HeatDiffusionSimulation

sim = HeatDiffusionSimulation(size=100, thermal_diffusivity=2.0)
sim.start_animation()
sim.show()
```
**Features**: 2D heat equation, temperature gradients, boundary conditions

#### Thermodynamic Cycles
```python
from physlib.s02_thermodynamics.visualizations import ThermodynamicCycle

# Carnot cycle
carnot = ThermodynamicCycle(cycle_type='carnot')
carnot.start_animation()
carnot.show()

# Otto cycle (internal combustion)
otto = ThermodynamicCycle(cycle_type='otto')
otto.start_animation()
otto.show()
```
**Features**: P-V diagrams, engine visualization, efficiency calculations

#### Entropy Concepts
```python
from physlib.s02_thermodynamics.visualizations import EntropyVisualization

viz = EntropyVisualization()
viz.show()
```
**Features**: Statistical mechanics, mixing entropy, phase transitions

---

## 3. Electromagnetism ⚡

### Available Visualizations

#### Electric Field Visualization
```python
from physlib.s03_electromagnetism.visualizations import ElectricFieldVisualization

viz = ElectricFieldVisualization()
viz.show()
```
**Features**: Point charges, dipoles, parallel plates, field superposition

#### Charged Particle Motion
```python
from physlib.s03_electromagnetism.visualizations import ChargedParticleMotion

# Cyclotron motion
sim = ChargedParticleMotion(field_type='cyclotron')
sim.start_animation()
sim.show()

# Crossed E and B fields
sim = ChargedParticleMotion(field_type='crossed_EB')
sim.start_animation()
sim.show()
```
**Features**: Lorentz force, cyclotron frequency, drift motion

#### Electromagnetic Waves
```python
from physlib.s03_electromagnetism.visualizations import ElectromagneticWave, ElectromagneticWave3D

# 2D wave propagation
wave_2d = ElectromagneticWave(wavelength=3.0, amplitude=1.5)
wave_2d.start_animation()
wave_2d.show()

# 3D wave visualization
wave_3d = ElectromagneticWave3D()
wave_3d.show_static()
```
**Features**: E and B field oscillations, wave propagation, polarization

#### Interactive Lorentz Force Demo
```python
from physlib.s03_electromagnetism.visualizations import create_lorentz_force_demo

demo = create_lorentz_force_demo()
demo.show()
```
**Features**: Parameter sliders, trajectory analysis, force visualization

---

## 4. Waves & Optics 🌊

### Available Visualizations

#### Wave Interference
```python
from physlib.s04_waves_optics.visualizations import WaveInterferenceSimulation

# Two-source interference
sources = [(0, 2), (0, -2)]
sim = WaveInterferenceSimulation(sources, wavelength=1.0)
sim.start_animation()
sim.show()
```
**Features**: Multiple sources, constructive/destructive interference, animation

#### Double-Slit Experiment
```python
from physlib.s04_waves_optics.visualizations import DoubleSlitExperiment

sim = DoubleSlitExperiment(slit_separation=2.0, wavelength=0.5)
sim.start_animation()
sim.show()
```
**Features**: Intensity patterns, wave propagation, screen detection

#### Reflection & Refraction
```python
from physlib.s04_waves_optics.visualizations import ReflectionRefractionDemo

demo = ReflectionRefractionDemo()
demo.show(incident_angle=45, n1=1.0, n2=1.5)
```
**Features**: Snell's law, critical angle, total internal reflection

#### Single-Slit Diffraction
```python
from physlib.s04_waves_optics.visualizations import DiffractionSimulation

sim = DiffractionSimulation(slit_width=2.0, wavelength=0.6)
sim.start_animation()
sim.show()
```
**Features**: Fraunhofer diffraction, intensity patterns, angular distribution

#### Interactive Wave Superposition
```python
from physlib.s04_waves_optics.visualizations import create_wave_superposition_demo

demo = create_wave_superposition_demo()
demo.show()
```
**Features**: Amplitude/frequency controls, beat phenomena, interference

---

## 5. Relativity 🚀

### Available Visualizations

#### Spacetime Diagrams
```python
from physlib.s05_relativity.visualizations import SpacetimeDiagram

diagrams = SpacetimeDiagram()
diagrams.show(v1=0.6, v2=0.8)  # Time dilation and length contraction
```
**Features**: Minkowski diagrams, world lines, simultaneity

#### Relativistic Motion
```python
from physlib.s05_relativity.visualizations import RelativisticMotion

# Constant proper acceleration
sim = RelativisticMotion(scenario='acceleration')
sim.start_animation()
sim.show()

# Twin paradox
twin_sim = RelativisticMotion(scenario='twin_paradox')
twin_sim.start_animation()
twin_sim.show()
```
**Features**: Lorentz factor evolution, proper time, aging effects

#### Gravitational Lensing
```python
from physlib.s05_relativity.visualizations import GravitationalLensing

lensing = GravitationalLensing()
lensing.show()
```
**Features**: Light bending, Einstein rings, deflection angles

#### Black Hole Physics
```python
from physlib.s05_relativity.visualizations import BlackHoleVisualization

bh_viz = BlackHoleVisualization()
bh_viz.show()
```
**Features**: Event horizons, tidal forces, accretion disks

#### Interactive Velocity Addition
```python
from physlib.s05_relativity.visualizations import create_relativistic_velocity_demo

demo = create_relativistic_velocity_demo()
demo.show()
```
**Features**: Classical vs relativistic addition, parameter exploration

---

## 6. Quantum Mechanics ⚛️

### Available Visualizations

#### Quantum Wave Packets
```python
from physlib.s06_quantum_mechanics.visualizations import QuantumWavePacket

sim = QuantumWavePacket(initial_position=-3, initial_momentum=2, sigma=0.5)
sim.start_animation()
sim.show()
```
**Features**: Wave function evolution, dispersion, probability density

#### Quantum Tunneling
```python
from physlib.s06_quantum_mechanics.visualizations import QuantumTunneling

sim = QuantumTunneling(barrier_height=3.0, barrier_width=1.5, particle_energy=2.0)
sim.start_animation()
sim.show()
```
**Features**: Barrier penetration, transmission coefficients, evanescent waves

#### Quantum Harmonic Oscillator
```python
from physlib.s06_quantum_mechanics.visualizations import QuantumHarmonicOscillator

sim = QuantumHarmonicOscillator(n_max=5)
sim.start_animation()
sim.show()
```
**Features**: Energy eigenstates, coherent states, time evolution

#### Uncertainty Principle
```python
from physlib.s06_quantum_mechanics.visualizations import UncertaintyPrincipleDemo

demo = UncertaintyPrincipleDemo()
demo.show()
```
**Features**: Position-momentum trade-offs, energy-time uncertainty, measurement

#### Interactive Quantum Measurement
```python
from physlib.s06_quantum_mechanics.visualizations import create_quantum_measurement_demo

demo = create_quantum_measurement_demo()
demo.show()
```
**Features**: State collapse, measurement operators, superposition

---

## 7. Astrophysics 🌌

### Available Visualizations

#### Cosmic Expansion
```python
from physlib.s07_astrophysics.visualizations import CosmicExpansion

sim = CosmicExpansion(n_galaxies=30, hubble_constant=70)
sim.start_animation()
sim.show()
```
**Features**: Hubble's law, scale factor evolution, galaxy recession

#### Black Hole Accretion
```python
from physlib.s07_astrophysics.visualizations import BlackHoleAccretion

sim = BlackHoleAccretion(black_hole_mass=10)  # 10 solar masses
sim.start_animation()
sim.show()
```
**Features**: Particle trajectories, temperature gradients, event horizons

#### Cosmic Microwave Background
```python
from physlib.s07_astrophysics.visualizations import CosmicMicrowaveBackground

cmb = CosmicMicrowaveBackground()
cmb.show()
```
**Features**: Temperature fluctuations, blackbody spectrum, universe timeline

#### Stellar Evolution
```python
from physlib.s07_astrophysics.visualizations import StellarEvolution

stellar = StellarEvolution()
stellar.show()
```
**Features**: HR diagram, evolutionary tracks, stellar lifecycles

#### Interactive Galaxy Collision
```python
from physlib.s07_astrophysics.visualizations import create_galaxy_collision_demo

demo = create_galaxy_collision_demo()
demo.show()
```
**Features**: N-body dynamics, tidal tails, merger simulation

---

## 🎛️ Interactive Features

### Parameter Control
Most visualizations support interactive parameter adjustment:

```python
from physlib.visualization import InteractivePhysicsPlot

plot = InteractivePhysicsPlot()
plot.add_slider('Parameter', min_val, max_val, initial_val, callback_function)
plot.add_button('Action', action_function)
plot.show()
```

### Animation Controls
Standard animation controls available:

```python
from physlib.visualization import AnimationControls

# Add play/pause/reset controls to any animation
controls = AnimationControls(your_animation)
```

### Custom Colormaps
Physics-appropriate color schemes:

```python
from physlib.visualization import ColorMaps

# Use predefined colormaps
plt.imshow(data, cmap=ColorMaps.TEMPERATURE)
plt.imshow(field, cmap=ColorMaps.ELECTRIC_FIELD)
plt.imshow(probability, cmap=ColorMaps.PROBABILITY)
```

---

## 🔧 Creating Custom Visualizations

### Basic Animation Framework
```python
from physlib.visualization import PhysicsAnimation

class MyPhysicsSimulation(PhysicsAnimation):
    def __init__(self, parameter1, parameter2):
        super().__init__(figsize=(10, 8))
        self.param1 = parameter1
        self.param2 = parameter2
        self.setup_physics()
        self.setup_plot()
    
    def setup_physics(self):
        # Initialize physics parameters
        pass
    
    def setup_plot(self):
        # Configure plot appearance
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_title('My Physics Simulation')
    
    def init_plot(self):
        # Initialize plot elements
        return self.plot_elements
    
    def animate(self, frame):
        # Update physics and plot for each frame
        # Update physics calculations here
        # Update plot elements
        return self.plot_elements

# Use your simulation
sim = MyPhysicsSimulation(param1=1.0, param2=2.0)
sim.start_animation(interval=50, frames=200)
sim.show()
```

### Adding Interactivity
```python
from physlib.visualization import InteractivePhysicsPlot

def create_interactive_demo():
    plot = InteractivePhysicsPlot()
    
    params = {'mass': 1.0, 'velocity': 2.0}
    
    def update_simulation(val=None):
        plot.main_ax.clear()
        # Your physics calculations using params
        # Update plot
        plot.fig.canvas.draw()
    
    plot.add_slider('Mass', 0.1, 10.0, params['mass'],
                   lambda val: (params.update({'mass': val}), update_simulation()))
    
    update_simulation()  # Initial plot
    return plot

demo = create_interactive_demo()
demo.show()
```

---

## 📊 Visualization Best Practices

### Performance Tips
- Use `blit=True` for smooth animations
- Limit data points for real-time updates
- Use appropriate frame rates (30-60 fps for smooth motion)

### Visual Clarity
- Choose appropriate colormaps for physical quantities
- Add clear labels and units
- Use consistent scaling across related plots
- Include legends and annotations

### Educational Effectiveness
- Start with simple cases, add complexity gradually
- Highlight key physics concepts visually
- Provide parameter ranges that show interesting behavior
- Include theoretical predictions for comparison

---

## 🚀 Advanced Examples

### Multi-Physics Comparison
```python
# Compare classical and quantum harmonic oscillators
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Classical oscillator
t = np.linspace(0, 4*np.pi, 200)
x_classical = np.cos(t)
ax1.plot(t, x_classical, 'b-', linewidth=2, label='Position')
ax1.set_title('Classical Harmonic Oscillator')

# Quantum oscillator probability
from physlib.s06_quantum_mechanics.visualizations import QuantumHarmonicOscillator
# ... quantum simulation code ...

plt.tight_layout()
plt.show()
```

### Custom Physics Integration
```python
# Combine multiple physics domains
from physlib.s01_classical_mechanics import gravity
from physlib.s05_relativity import special

def relativistic_orbit_simulation():
    # Classical gravitational force
    F_gravity = gravity.gravitational_force(m1, m2, r)
    
    # Relativistic corrections
    gamma = special.lorentz_factor(v)
    
    # Combined physics simulation
    # ... implementation ...
```

---

## 🎯 Educational Applications

### Classroom Demonstrations
- Project visualizations for class discussion
- Use interactive controls to explore "what if" scenarios
- Compare predictions with experimental data

### Laboratory Exercises
- Validate theoretical predictions
- Explore parameter dependencies
- Investigate limiting cases and approximations

### Self-Study
- Work through physics concepts visually
- Test understanding with parameter variations
- Explore connections between different physics domains

---

## 🔍 Troubleshooting

### Common Issues

#### Animation Not Displaying
```python
# Ensure proper backend
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

#### Slow Performance
```python
# Reduce data points or frame rate
sim.start_animation(interval=100, frames=100)  # Slower updates
```

#### Import Errors
```bash
# Install visualization dependencies
pip install -e .[visualization]
```

### Getting Help
- Check function docstrings for parameter details
- Review example usage in demonstration functions
- Refer to physics textbooks for concept explanations

---

**Happy Visualizing!** 🌟 Explore the beauty of physics through interactive simulations and animations.