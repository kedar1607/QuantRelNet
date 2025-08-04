"""Visual simulations for thermodynamics concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import LineCollection
from typing import List, Tuple, Optional
from ..visualization import PhysicsAnimation, ParticleTracker, setup_physics_plot, ColorMaps, InteractivePhysicsPlot
from . import laws, heat_transfer, entropy


class GasParticleSimulation(PhysicsAnimation):
    """Simulate kinetic theory of gases with temperature visualization."""
    
    def __init__(self, n_particles: int = 100, temperature: float = 300.0, 
                 box_size: float = 10.0, figsize=(12, 8)):
        super().__init__(figsize)
        self.n_particles = n_particles
        self.temperature = temperature
        self.box_size = box_size
        self.dt = 0.02
        
        # Physical constants
        self.k_b = 1.380649e-23  # Boltzmann constant
        self.particle_mass = 4.65e-26  # Approximate for nitrogen molecule
        
        # Initialize particles
        self.positions = np.random.uniform(-box_size/2, box_size/2, (n_particles, 2))
        self.velocities = self.maxwell_boltzmann_velocities()
        
        # Visualization elements
        self.particles = self.ax.scatter([], [], s=20, c=[], cmap='hot', vmin=0, vmax=2000, alpha=0.7)
        
        # Box walls
        self.box_lines = []
        wall_coords = [
            [[-box_size/2, box_size/2], [-box_size/2, -box_size/2]],  # left
            [[box_size/2, box_size/2], [box_size/2, -box_size/2]],    # right
            [[-box_size/2, -box_size/2], [box_size/2, -box_size/2]],  # bottom
            [[-box_size/2, box_size/2], [box_size/2, box_size/2]]     # top
        ]
        
        for wall in wall_coords:
            line, = self.ax.plot([wall[0][0], wall[1][0]], [wall[0][1], wall[1][1]], 'k-', lw=3)
            self.box_lines.append(line)
            
        self.setup_plot()
        
    def maxwell_boltzmann_velocities(self) -> np.ndarray:
        """Generate velocities from Maxwell-Boltzmann distribution."""
        # Standard deviation of velocity distribution
        sigma = np.sqrt(self.k_b * self.temperature / self.particle_mass)
        
        # Generate random velocities
        velocities = np.random.normal(0, sigma, (self.n_particles, 2))
        return velocities
        
    def setup_plot(self):
        """Configure plot appearance."""
        margin = self.box_size * 0.6
        self.ax.set_xlim(-margin, margin)
        self.ax.set_ylim(-margin, margin)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('Position (m)')
        self.ax.set_ylabel('Position (m)')
        self.ax.set_title(f'Kinetic Theory of Gases (T={self.temperature:.0f}K, N={self.n_particles})')
        
        # Add colorbar for speed
        cbar = plt.colorbar(self.particles, ax=self.ax)
        cbar.set_label('Speed (m/s)', rotation=270, labelpad=15)
        
        # Add temperature display
        self.temp_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     verticalalignment='top', fontsize=10, 
                                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
    def handle_wall_collisions(self):
        """Handle elastic collisions with walls."""
        half_box = self.box_size / 2
        
        # Left and right walls
        left_collision = self.positions[:, 0] <= -half_box
        right_collision = self.positions[:, 0] >= half_box
        self.velocities[left_collision | right_collision, 0] *= -1
        self.positions[left_collision, 0] = -half_box
        self.positions[right_collision, 0] = half_box
        
        # Bottom and top walls
        bottom_collision = self.positions[:, 1] <= -half_box
        top_collision = self.positions[:, 1] >= half_box
        self.velocities[bottom_collision | top_collision, 1] *= -1
        self.positions[bottom_collision, 1] = -half_box
        self.positions[top_collision, 1] = half_box
        
    def calculate_temperature(self) -> float:
        """Calculate instantaneous temperature from kinetic energy."""
        kinetic_energies = 0.5 * self.particle_mass * np.sum(self.velocities**2, axis=1)
        avg_kinetic_energy = np.mean(kinetic_energies)
        # From equipartition theorem: <E_k> = (f/2)k_B*T, where f=2 for 2D
        return avg_kinetic_energy / self.k_b
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.particles] + self.box_lines
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Update positions
        self.positions += self.velocities * self.dt
        
        # Handle wall collisions
        self.handle_wall_collisions()
        
        # Calculate particle speeds for coloring
        speeds = np.linalg.norm(self.velocities, axis=1)
        
        # Update particle display
        self.particles.set_offsets(self.positions)
        self.particles.set_array(speeds)
        
        # Update temperature display
        current_temp = self.calculate_temperature()
        avg_speed = np.mean(speeds)
        self.temp_text.set_text(
            f'Temperature: {current_temp:.0f} K\n'
            f'Avg Speed: {avg_speed:.1f} m/s\n'
            f'Target Temp: {self.temperature:.0f} K'
        )
        
        return [self.particles] + self.box_lines


class HeatDiffusionSimulation(PhysicsAnimation):
    """Visualize heat diffusion in a 2D material."""
    
    def __init__(self, size: int = 50, thermal_diffusivity: float = 1.0, figsize=(10, 8)):
        super().__init__(figsize)
        self.size = size
        self.alpha = thermal_diffusivity  # Thermal diffusivity
        self.dt = 0.01
        self.dx = 1.0
        
        # Initialize temperature field
        self.temperature = np.zeros((size, size))
        self.setup_initial_conditions()
        
        # Visualization
        self.im = self.ax.imshow(self.temperature, cmap=ColorMaps.TEMPERATURE, 
                                vmin=0, vmax=100, animated=True)
        
        self.setup_plot()
        
    def setup_initial_conditions(self):
        """Set up initial temperature distribution."""
        # Hot spot in the center
        center = self.size // 2
        radius = self.size // 8
        y, x = np.ogrid[:self.size, :self.size]
        mask = (x - center)**2 + (y - center)**2 <= radius**2
        self.temperature[mask] = 100.0
        
        # Cold boundaries
        self.temperature[0, :] = 0.0   # top
        self.temperature[-1, :] = 0.0  # bottom
        self.temperature[:, 0] = 0.0   # left
        self.temperature[:, -1] = 0.0  # right
        
    def setup_plot(self):
        """Configure plot appearance."""
        self.ax.set_title('Heat Diffusion in 2D Material')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        
        # Add colorbar
        cbar = plt.colorbar(self.im, ax=self.ax)
        cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)
        
        # Remove ticks for cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
    def diffusion_step(self):
        """Apply one step of heat diffusion equation."""
        # Heat equation: ∂T/∂t = α∇²T
        # Finite difference approximation
        T = self.temperature.copy()
        
        # Calculate Laplacian (∇²T)
        laplacian = (
            np.roll(T, 1, axis=0) + np.roll(T, -1, axis=0) +
            np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) - 4*T
        ) / (self.dx**2)
        
        # Update temperature
        self.temperature += self.alpha * self.dt * laplacian
        
        # Maintain boundary conditions (constant temperature boundaries)
        self.temperature[0, :] = 0.0
        self.temperature[-1, :] = 0.0
        self.temperature[:, 0] = 0.0
        self.temperature[:, -1] = 0.0
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.setup_initial_conditions()
        self.im.set_array(self.temperature)
        return [self.im]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Multiple diffusion steps per frame for faster animation
        for _ in range(5):
            self.diffusion_step()
            
        self.im.set_array(self.temperature)
        return [self.im]


class ThermodynamicCycle(PhysicsAnimation):
    """Visualize thermodynamic cycles (Carnot, Otto, etc.)."""
    
    def __init__(self, cycle_type: str = 'carnot', figsize=(12, 5)):
        super().__init__(figsize)
        self.cycle_type = cycle_type.lower()
        self.frame_count = 0
        self.cycle_complete = False
        
        # Cycle parameters
        if cycle_type == 'carnot':
            self.setup_carnot_cycle()
        elif cycle_type == 'otto':
            self.setup_otto_cycle()
        else:
            raise ValueError("Supported cycles: 'carnot', 'otto'")
            
        self.setup_plot()
        
    def setup_carnot_cycle(self):
        """Set up Carnot cycle parameters."""
        # Carnot cycle: isothermal expansion, adiabatic expansion, 
        # isothermal compression, adiabatic compression
        self.T_hot = 600  # K
        self.T_cold = 300  # K
        self.V_min = 1.0
        self.V_max = 4.0
        
        # Generate cycle path
        self.generate_carnot_path()
        
    def setup_otto_cycle(self):
        """Set up Otto cycle parameters."""
        # Otto cycle: adiabatic compression, isochoric heating,
        # adiabatic expansion, isochoric cooling
        self.compression_ratio = 8
        self.V_min = 1.0
        self.V_max = self.V_min * self.compression_ratio
        self.T_min = 300  # K
        self.T_max = 1200  # K
        
        # Generate cycle path
        self.generate_otto_path()
        
    def generate_carnot_path(self):
        """Generate P-V data for Carnot cycle."""
        n_points = 100
        
        # Process 1: Isothermal expansion at T_hot
        V1 = np.linspace(self.V_min, self.V_max/2, n_points//4)
        P1 = self.T_hot / V1  # Ideal gas: PV = nRT, assuming nR = 1
        
        # Process 2: Adiabatic expansion
        V2 = np.linspace(self.V_max/2, self.V_max, n_points//4)
        P2 = P1[-1] * (V1[-1]/V2)**(5/3)  # γ = 5/3 for ideal gas
        
        # Process 3: Isothermal compression at T_cold
        V3 = np.linspace(self.V_max, self.V_max/2, n_points//4)
        P3 = self.T_cold / V3
        
        # Process 4: Adiabatic compression
        V4 = np.linspace(self.V_max/2, self.V_min, n_points//4)
        P4 = P3[-1] * (V3[-1]/V4)**(5/3)
        
        # Combine all processes
        self.volumes = np.concatenate([V1, V2, V3, V4])
        self.pressures = np.concatenate([P1, P2, P3, P4])
        
    def generate_otto_path(self):
        """Generate P-V data for Otto cycle."""
        n_points = 100
        gamma = 1.4  # Heat capacity ratio for air
        
        # Process 1: Adiabatic compression
        V1 = np.linspace(self.V_max, self.V_min, n_points//4)
        P1 = (V1[0]/V1)**gamma  # Starting at P=1
        
        # Process 2: Isochoric heating
        V2 = np.full(n_points//4, self.V_min)
        P2 = np.linspace(P1[-1], P1[-1] * (self.T_max/self.T_min), n_points//4)
        
        # Process 3: Adiabatic expansion
        V3 = np.linspace(self.V_min, self.V_max, n_points//4)
        P3 = P2[-1] * (V2[-1]/V3)**gamma
        
        # Process 4: Isochoric cooling
        V4 = np.full(n_points//4, self.V_max)
        P4 = np.linspace(P3[-1], 1.0, n_points//4)
        
        # Combine all processes
        self.volumes = np.concatenate([V1, V2, V3, V4])
        self.pressures = np.concatenate([P1, P2, P3, P4])
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Create subplots for P-V diagram and cycle illustration
        self.fig.clear()
        self.ax_pv = self.fig.add_subplot(121)
        self.ax_cycle = self.fig.add_subplot(122)
        
        # P-V diagram
        self.ax_pv.set_xlabel('Volume (L)')
        self.ax_pv.set_ylabel('Pressure (atm)')
        self.ax_pv.set_title(f'{self.cycle_type.capitalize()} Cycle - P-V Diagram')
        self.ax_pv.grid(True, alpha=0.3)
        
        # Plot full cycle (faded)
        self.ax_pv.plot(self.volumes, self.pressures, 'k--', alpha=0.3, linewidth=1)
        
        # Current position marker
        self.current_point, = self.ax_pv.plot([], [], 'ro', markersize=8)
        self.traced_line, = self.ax_pv.plot([], [], 'b-', linewidth=3)
        
        # Cycle illustration
        self.ax_cycle.set_xlim(-2, 2)
        self.ax_cycle.set_ylim(-2, 2)
        self.ax_cycle.set_aspect('equal')
        self.ax_cycle.set_title('Engine Cycle Visualization')
        self.ax_cycle.set_xticks([])
        self.ax_cycle.set_yticks([])
        
        # Draw engine components
        cylinder = Rectangle((-1, -1.5), 2, 3, fill=False, linewidth=3)
        self.ax_cycle.add_patch(cylinder)
        
        # Piston (will be animated)
        self.piston = Rectangle((-0.9, 0), 1.8, 0.2, facecolor='gray')
        self.ax_cycle.add_patch(self.piston)
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.frame_count = 0
        self.cycle_complete = False
        return [self.current_point, self.traced_line, self.piston]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        if frame >= len(self.volumes):
            frame = frame % len(self.volumes)
            
        # Update P-V diagram
        current_V = self.volumes[:frame+1]
        current_P = self.pressures[:frame+1]
        
        self.current_point.set_data([self.volumes[frame]], [self.pressures[frame]])
        self.traced_line.set_data(current_V, current_P)
        
        # Update piston position (normalize volume to piston range)
        piston_pos = -1.3 + 1.6 * (self.volumes[frame] - self.V_min) / (self.V_max - self.V_min)
        self.piston.set_xy((-0.9, piston_pos))
        
        return [self.current_point, self.traced_line, self.piston]


class EntropyVisualization:
    """Interactive visualization of entropy concepts."""
    
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 10))
        self.axes = self.axes.flatten()
        
    def plot_mixing_entropy(self):
        """Visualize entropy increase during gas mixing."""
        ax = self.axes[0]
        
        # Create two-compartment box
        box_width, box_height = 10, 5
        
        # Initially separated gases
        n_particles_A = 50
        n_particles_B = 50
        
        # Positions for separated state
        pos_A_sep = np.random.uniform([0, 0], [box_width/2, box_height], (n_particles_A, 2))
        pos_B_sep = np.random.uniform([box_width/2, 0], [box_width, box_height], (n_particles_B, 2))
        
        # Positions for mixed state
        pos_A_mix = np.random.uniform([0, 0], [box_width, box_height], (n_particles_A, 2))
        pos_B_mix = np.random.uniform([0, 0], [box_width, box_height], (n_particles_B, 2))
        
        # Plot separated state
        ax.scatter(pos_A_sep[:, 0], pos_A_sep[:, 1], c='red', alpha=0.6, s=20, label='Gas A')
        ax.scatter(pos_B_sep[:, 0], pos_B_sep[:, 1], c='blue', alpha=0.6, s=20, label='Gas B')
        
        # Draw separator
        ax.axvline(x=box_width/2, color='black', linewidth=3)
        
        # Box outline
        ax.add_patch(Rectangle((0, 0), box_width, box_height, fill=False, linewidth=2))
        
        ax.set_xlim(-1, box_width+1)
        ax.set_ylim(-1, box_height+1)
        ax.set_title('Initial State: Separated Gases\nLow Entropy')
        ax.legend()
        ax.set_aspect('equal')
        
        # Calculate and display entropy
        S_initial = entropy.mixing_entropy([n_particles_A, n_particles_B], separated=True)
        ax.text(0.02, 0.98, f'S = {S_initial:.2e} J/K', transform=ax.transAxes, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
               
    def plot_temperature_entropy(self):
        """Plot entropy vs temperature relationship."""
        ax = self.axes[1]
        
        temperatures = np.linspace(100, 1000, 100)
        
        # Different materials with different heat capacities
        materials = {
            'Water': {'Cp': 4186, 'color': 'blue'},
            'Iron': {'Cp': 449, 'color': 'red'},
            'Air': {'Cp': 1005, 'color': 'green'}
        }
        
        T_ref = 298  # Reference temperature (K)
        
        for material, props in materials.items():
            # S(T) = S(T_ref) + Cp * ln(T/T_ref) for constant Cp
            entropies = props['Cp'] * np.log(temperatures / T_ref)
            ax.plot(temperatures, entropies, color=props['color'], linewidth=2, label=material)
            
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Entropy Change (J/K)')
        ax.set_title('Entropy vs Temperature')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_phase_transition_entropy(self):
        """Show entropy jump at phase transitions."""
        ax = self.axes[2]
        
        # Water phase transitions
        temperatures = np.linspace(250, 450, 1000)
        entropies = np.zeros_like(temperatures)
        
        # Ice phase (T < 273K)
        ice_mask = temperatures < 273
        entropies[ice_mask] = 2.1 * (temperatures[ice_mask] - 273)  # Simplified
        
        # Melting point jump
        melt_mask = (temperatures >= 273) & (temperatures < 274)
        entropies[melt_mask] = 22.0  # Latent heat of fusion / T
        
        # Liquid water (273K < T < 373K)
        liquid_mask = (temperatures >= 274) & (temperatures < 373)
        entropies[liquid_mask] = 22.0 + 4.18 * np.log(temperatures[liquid_mask] / 273)
        
        # Boiling point jump
        boil_mask = (temperatures >= 373) & (temperatures < 374)
        entropies[boil_mask] = entropies[liquid_mask][-1] + 109  # Latent heat of vaporization / T
        
        # Steam (T > 373K)
        steam_mask = temperatures >= 374
        entropies[steam_mask] = entropies[boil_mask][-1] + 2.01 * np.log(temperatures[steam_mask] / 373)
        
        ax.plot(temperatures, entropies, 'b-', linewidth=2)
        ax.axvline(273, color='red', linestyle='--', alpha=0.7, label='Melting Point')
        ax.axvline(373, color='red', linestyle='--', alpha=0.7, label='Boiling Point')
        
        ax.set_xlabel('Temperature (K)')
        ax.set_ylabel('Entropy (J/mol·K)')
        ax.set_title('Entropy Changes in Water Phase Transitions')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_irreversible_process(self):
        """Visualize entropy production in irreversible processes."""
        ax = self.axes[3]
        
        # Free expansion of gas
        times = np.linspace(0, 10, 100)
        
        # Initial state: gas confined to half the volume
        V_initial = 1.0
        V_final = 2.0
        
        # Volume expansion (exponential approach to equilibrium)
        volumes = V_final - (V_final - V_initial) * np.exp(-times)
        
        # Entropy change: ΔS = nR ln(V_f/V_i)
        R = 8.314  # J/mol·K
        n = 1  # 1 mole
        entropies = n * R * np.log(volumes / V_initial)
        
        ax.plot(times, entropies, 'g-', linewidth=3, label='Entropy')
        ax.axhline(n * R * np.log(V_final / V_initial), color='red', linestyle='--', 
                  label='Final Entropy')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Entropy Change (J/K)')
        ax.set_title('Entropy Production in Free Expansion')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def show(self):
        """Display all entropy visualizations."""
        self.plot_mixing_entropy()
        self.plot_temperature_entropy()
        self.plot_phase_transition_entropy()
        self.plot_irreversible_process()
        
        plt.tight_layout()
        plt.show()


# Convenience functions for quick demonstrations
def demo_gas_particles():
    """Quick gas particle simulation demo."""
    sim = GasParticleSimulation(n_particles=150, temperature=400)
    sim.start_animation(interval=30, frames=1000)
    sim.show()

def demo_heat_diffusion():
    """Quick heat diffusion demo."""
    sim = HeatDiffusionSimulation(size=60, thermal_diffusivity=2.0)
    sim.start_animation(interval=50, frames=500)
    sim.show()

def demo_carnot_cycle():
    """Quick Carnot cycle demo."""
    sim = ThermodynamicCycle(cycle_type='carnot')
    sim.start_animation(interval=100, frames=400)
    sim.show()

def demo_otto_cycle():
    """Quick Otto cycle demo."""
    sim = ThermodynamicCycle(cycle_type='otto')
    sim.start_animation(interval=100, frames=400)
    sim.show()

def demo_entropy():
    """Quick entropy visualization demo."""
    viz = EntropyVisualization()
    viz.show()