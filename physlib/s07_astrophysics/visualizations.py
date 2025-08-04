"""Visual simulations for astrophysics concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Optional, Callable
from ..visualization import PhysicsAnimation, setup_physics_plot, ColorMaps, create_3d_axes, InteractivePhysicsPlot
from . import big_bang, black_holes, standard_model


class CosmicExpansion(PhysicsAnimation):
    """Visualize cosmic expansion and Hubble's law."""
    
    def __init__(self, n_galaxies: int = 20, hubble_constant: float = 70.0, figsize=(12, 8)):
        super().__init__(figsize)
        self.n_galaxies = n_galaxies
        self.H0 = hubble_constant  # km/s/Mpc
        self.dt = 0.05  # Time step in billions of years
        
        # Create subplots
        self.fig.clear()
        self.ax_expansion = self.fig.add_subplot(121)
        self.ax_hubble = self.fig.add_subplot(122)
        
        # Galaxy positions (initial distances from observer)
        np.random.seed(42)  # For reproducible positions
        self.initial_distances = np.random.uniform(10, 100, n_galaxies)  # Mpc
        self.galaxy_angles = np.random.uniform(0, 2*np.pi, n_galaxies)
        
        # Colors for different galaxy types
        self.galaxy_colors = np.random.choice(['blue', 'red', 'yellow', 'white'], n_galaxies)
        
        # Plot elements
        self.galaxy_scatter = self.ax_expansion.scatter([], [], s=[], c=[], alpha=0.8, animated=True)
        self.hubble_line, = self.ax_hubble.plot([], [], 'ro', markersize=6, animated=True)
        self.hubble_fit_line, = self.ax_hubble.plot([], [], 'b-', linewidth=2, animated=True)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Expansion visualization
        self.ax_expansion.set_xlim(-150, 150)
        self.ax_expansion.set_ylim(-150, 150)
        self.ax_expansion.set_aspect('equal')
        self.ax_expansion.set_xlabel('Distance (Mpc)')
        self.ax_expansion.set_ylabel('Distance (Mpc)')
        self.ax_expansion.set_title('Cosmic Expansion')
        
        # Observer at center
        self.ax_expansion.scatter(0, 0, s=200, c='green', marker='*', 
                                 label='Observer (Earth)', zorder=5)
        self.ax_expansion.legend()
        
        # Hubble diagram
        self.ax_hubble.set_xlim(0, 150)
        self.ax_hubble.set_ylim(0, 10000)
        self.ax_hubble.set_xlabel('Distance (Mpc)')
        self.ax_hubble.set_ylabel('Recession Velocity (km/s)')
        self.ax_hubble.set_title(f'Hubble\'s Law (H₀ = {self.H0} km/s/Mpc)')
        self.ax_hubble.grid(True, alpha=0.3)
        
        # Add time display
        self.time_text = self.ax_expansion.text(0.02, 0.98, '', transform=self.ax_expansion.transAxes,
                                               fontsize=12, verticalalignment='top',
                                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
    def scale_factor(self, t: float) -> float:
        """Calculate scale factor as function of time (simplified)."""
        # For matter-dominated universe: a(t) ∝ t^(2/3)
        # For Lambda-dominated: a(t) ∝ exp(H*t)
        # Use mixed model
        if t < 5:  # Early universe - matter dominated
            return (t + 0.1)**(2/3)
        else:  # Late universe - dark energy dominated
            return (5.1)**(2/3) * np.exp(self.H0 * 1e-3 * (t - 5))
            
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.galaxy_scatter, self.hubble_line, self.hubble_fit_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * self.dt  # Time in billion years
        
        # Current scale factor
        a = self.scale_factor(t)
        
        # Current galaxy positions
        current_distances = self.initial_distances * a
        galaxy_x = current_distances * np.cos(self.galaxy_angles)
        galaxy_y = current_distances * np.sin(self.galaxy_angles)
        
        # Galaxy sizes (closer galaxies appear larger)
        sizes = 100 / (1 + current_distances / 50)
        
        # Update expansion plot
        self.galaxy_scatter.set_offsets(np.column_stack([galaxy_x, galaxy_y]))
        self.galaxy_scatter.set_sizes(sizes)
        self.galaxy_scatter.set_color(self.galaxy_colors)
        
        # Calculate recession velocities (Hubble's law: v = H₀ * d)
        recession_velocities = self.H0 * current_distances
        
        # Update Hubble diagram
        self.hubble_line.set_data(current_distances, recession_velocities)
        
        # Fit line for Hubble's law
        distance_range = np.linspace(0, np.max(current_distances), 100)
        velocity_fit = self.H0 * distance_range
        self.hubble_fit_line.set_data(distance_range, velocity_fit)
        
        # Update time display
        self.time_text.set_text(f'Time: {t:.1f} billion years\nScale factor: {a:.2f}')
        
        return [self.galaxy_scatter, self.hubble_line, self.hubble_fit_line]


class BlackHoleAccretion(PhysicsAnimation):
    """Visualize matter falling into a black hole."""
    
    def __init__(self, black_hole_mass: float = 10.0, figsize=(10, 10)):
        super().__init__(figsize)
        self.M_bh = black_hole_mass  # Solar masses
        self.G = 4.3e-3  # Gravitational constant in pc * (km/s)^2 / M_sun
        self.c = 3e5  # Speed of light in km/s
        self.dt = 0.1
        
        # Schwarzschild radius in parsecs
        self.rs = 2 * self.G * self.M_bh / self.c**2
        
        # Create matter particles
        self.n_particles = 50
        np.random.seed(42)
        
        # Initialize particle positions and velocities
        self.reset_particles()
        
        # Visualization elements
        self.particles_scatter = self.ax.scatter([], [], s=[], c=[], cmap='hot', 
                                                vmin=0, vmax=1000, alpha=0.8, animated=True)
        
        self.setup_plot()
        
    def reset_particles(self):
        """Reset particle positions and velocities."""
        # Initial positions (random around black hole)
        distances = np.random.uniform(5*self.rs, 20*self.rs, self.n_particles)
        angles = np.random.uniform(0, 2*np.pi, self.n_particles)
        
        self.positions = np.column_stack([
            distances * np.cos(angles),
            distances * np.sin(angles)
        ])
        
        # Initial velocities (mostly tangential for stable orbits)
        orbital_velocities = np.sqrt(self.G * self.M_bh / distances)
        velocity_angles = angles + np.pi/2  # Perpendicular to radial direction
        
        # Add some randomness to create unstable orbits
        velocity_magnitudes = orbital_velocities * np.random.uniform(0.3, 0.8, self.n_particles)
        
        self.velocities = np.column_stack([
            velocity_magnitudes * np.cos(velocity_angles),
            velocity_magnitudes * np.sin(velocity_angles)
        ])
        
        # Particle masses (for color coding temperature/energy)
        self.particle_masses = np.random.uniform(0.1, 2.0, self.n_particles)
        
    def setup_plot(self):
        """Configure plot appearance."""
        plot_range = 30 * self.rs
        self.ax.set_xlim(-plot_range, plot_range)
        self.ax.set_ylim(-plot_range, plot_range)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('Distance (Schwarzschild radii)')
        self.ax.set_ylabel('Distance (Schwarzschild radii)')
        self.ax.set_title(f'Black Hole Accretion (M = {self.M_bh} M☉)')
        
        # Draw black hole
        bh_circle = Circle((0, 0), self.rs, color='black', zorder=5)
        self.ax.add_patch(bh_circle)
        
        # Draw event horizon
        horizon_circle = Circle((0, 0), self.rs, fill=False, color='red', 
                               linewidth=3, linestyle='--', zorder=4, label='Event Horizon')
        self.ax.add_patch(horizon_circle)
        
        # Draw photon sphere
        photon_sphere = Circle((0, 0), 1.5*self.rs, fill=False, color='orange', 
                              linewidth=2, linestyle=':', zorder=3, label='Photon Sphere')
        self.ax.add_patch(photon_sphere)
        
        # Draw ISCO (Innermost Stable Circular Orbit)
        isco_circle = Circle((0, 0), 3*self.rs, fill=False, color='yellow', 
                            linewidth=2, linestyle='-.', zorder=3, label='ISCO')
        self.ax.add_patch(isco_circle)
        
        self.ax.legend()
        
        # Add colorbar for particle temperature/energy
        cbar = plt.colorbar(self.particles_scatter, ax=self.ax)
        cbar.set_label('Temperature/Energy', rotation=270, labelpad=15)
        
    def gravitational_acceleration(self, positions: np.ndarray) -> np.ndarray:
        """Calculate gravitational acceleration for each particle."""
        accelerations = np.zeros_like(positions)
        
        for i, pos in enumerate(positions):
            r = np.linalg.norm(pos)
            if r > self.rs:  # Outside event horizon
                # Newtonian gravity (simplified)
                acc_magnitude = -self.G * self.M_bh / r**2
                acc_direction = pos / r
                accelerations[i] = acc_magnitude * acc_direction
            else:
                # Inside event horizon - no escape
                accelerations[i] = [0, 0]
                
        return accelerations
        
    def calculate_temperatures(self, positions: np.ndarray, velocities: np.ndarray) -> np.ndarray:
        """Calculate particle temperatures based on kinetic energy and position."""
        # Temperature increases as particles fall deeper into potential well
        kinetic_energies = 0.5 * self.particle_masses[:, np.newaxis] * np.sum(velocities**2, axis=1)
        
        distances = np.linalg.norm(positions, axis=1)
        potential_energies = -self.G * self.M_bh * self.particle_masses / np.maximum(distances, self.rs)
        
        # Higher kinetic energy and deeper potential = higher temperature
        temperatures = (kinetic_energies.flatten() - potential_energies) / self.particle_masses
        
        # Normalize for visualization
        temperatures = np.maximum(temperatures, 0)
        temperatures = 1000 * temperatures / np.max(temperatures) if np.max(temperatures) > 0 else temperatures
        
        return temperatures
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.reset_particles()
        return [self.particles_scatter]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Calculate forces
        accelerations = self.gravitational_acceleration(self.positions)
        
        # Update velocities and positions (Verlet integration)
        self.velocities += accelerations * self.dt
        self.positions += self.velocities * self.dt
        
        # Remove particles that have fallen into the black hole
        distances = np.linalg.norm(self.positions, axis=1)
        alive_mask = distances > self.rs
        
        # Keep only surviving particles
        self.positions = self.positions[alive_mask]
        self.velocities = self.velocities[alive_mask]
        self.particle_masses = self.particle_masses[alive_mask]
        
        # Add new particles to maintain count
        n_lost = self.n_particles - len(self.positions)
        if n_lost > 0:
            # Add new particles from the outer boundary
            new_distances = np.random.uniform(18*self.rs, 25*self.rs, n_lost)
            new_angles = np.random.uniform(0, 2*np.pi, n_lost)
            
            new_positions = np.column_stack([
                new_distances * np.cos(new_angles),
                new_distances * np.sin(new_angles)
            ])
            
            # Give them roughly circular velocities
            orbital_vels = np.sqrt(self.G * self.M_bh / new_distances)
            vel_angles = new_angles + np.pi/2
            orbital_vels *= np.random.uniform(0.4, 0.7, n_lost)
            
            new_velocities = np.column_stack([
                orbital_vels * np.cos(vel_angles),
                orbital_vels * np.sin(vel_angles)
            ])
            
            new_masses = np.random.uniform(0.1, 2.0, n_lost)
            
            # Append new particles
            self.positions = np.vstack([self.positions, new_positions])
            self.velocities = np.vstack([self.velocities, new_velocities])
            self.particle_masses = np.concatenate([self.particle_masses, new_masses])
        
        # Calculate temperatures for coloring
        temperatures = self.calculate_temperatures(self.positions, self.velocities)
        
        # Particle sizes based on mass
        sizes = 20 + 30 * self.particle_masses
        
        # Update scatter plot
        self.particles_scatter.set_offsets(self.positions)
        self.particles_scatter.set_sizes(sizes)
        self.particles_scatter.set_array(temperatures)
        
        return [self.particles_scatter]


class CosmicMicrowaveBackground:
    """Visualize the cosmic microwave background and its significance."""
    
    def __init__(self, figsize=(15, 5)):
        self.fig, self.axes = plt.subplots(1, 3, figsize=figsize)
        
    def plot_cmb_temperature_map(self, ax):
        """Plot simulated CMB temperature fluctuations."""
        # Create a simplified CMB-like temperature map
        size = 200
        
        # Generate correlated noise (simplified)
        np.random.seed(42)
        
        # Large scale structure
        large_scale = np.random.normal(0, 1, (size//4, size//4))
        large_scale = np.kron(large_scale, np.ones((4, 4)))
        
        # Medium scale structure
        medium_scale = np.random.normal(0, 0.5, (size//2, size//2))
        medium_scale = np.kron(medium_scale, np.ones((2, 2)))
        
        # Small scale structure
        small_scale = np.random.normal(0, 0.2, (size, size))
        
        # Combine scales
        temperature_map = large_scale + medium_scale + small_scale
        
        # Apply spherical projection effects (simplified)
        y, x = np.ogrid[:size, :size]
        center_y, center_x = size//2, size//2
        
        # Distance from center (for projection effects)
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # Suppress fluctuations near edges (projection artifacts)
        edge_factor = np.exp(-distance**2 / (size/3)**2)
        temperature_map *= edge_factor
        
        # Scale to microkelvin variations
        temperature_map = temperature_map * 100e-6  # 100 microkelvin variations
        
        # Plot
        im = ax.imshow(temperature_map, cmap=ColorMaps.TEMPERATURE, 
                      extent=[-180, 180, -90, 90], aspect='equal')
        
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        ax.set_title('Cosmic Microwave Background\nTemperature Fluctuations')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('ΔT (μK)', rotation=270, labelpad=15)
        
    def plot_cmb_spectrum(self, ax):
        """Plot CMB blackbody spectrum."""
        # Frequency range
        frequency = np.logspace(8, 12, 1000)  # Hz
        
        # CMB temperature
        T_cmb = 2.725  # Kelvin
        
        # Planck's law constants
        h = 6.626e-34  # Planck constant
        c = 3e8        # Speed of light
        k_b = 1.381e-23  # Boltzmann constant
        
        # Planck function
        x = h * frequency / (k_b * T_cmb)
        planck_intensity = (2 * h * frequency**3 / c**2) / (np.exp(x) - 1)
        
        # Plot spectrum
        ax.loglog(frequency / 1e9, planck_intensity, 'b-', linewidth=3, label=f'CMB (T = {T_cmb} K)')
        
        # Mark peak frequency
        peak_frequency = 2.82 * k_b * T_cmb / h  # Wien's displacement law
        peak_intensity = (2 * h * peak_frequency**3 / c**2) / (np.exp(2.82) - 1)
        
        ax.scatter([peak_frequency / 1e9], [peak_intensity], s=100, c='red', 
                  zorder=5, label=f'Peak at {peak_frequency/1e9:.0f} GHz')
        
        # Compare with other temperatures
        for T, color, alpha in [(100, 'orange', 0.5), (10, 'green', 0.5)]:
            x_comp = h * frequency / (k_b * T)
            planck_comp = (2 * h * frequency**3 / c**2) / (np.exp(x_comp) - 1)
            ax.loglog(frequency / 1e9, planck_comp, color=color, linewidth=2, 
                     alpha=alpha, linestyle='--', label=f'T = {T} K')
        
        ax.set_xlabel('Frequency (GHz)')
        ax.set_ylabel('Intensity (W⋅m⁻²⋅Hz⁻¹⋅sr⁻¹)')
        ax.set_title('CMB Blackbody Spectrum')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_universe_timeline(self, ax):
        """Plot timeline of universe evolution."""
        # Time periods (logarithmic scale)
        times = np.array([1e-43, 1e-36, 1e-12, 1e-6, 1, 380000, 1e9, 13.8e9])  # years
        
        events = [
            'Planck Era',
            'Inflation',
            'Electroweak\nUnification',
            'Quark\nConfinement',
            'Nucleosynthesis',
            'Recombination\n(CMB)',
            'First Stars',
            'Today'
        ]
        
        colors = ['purple', 'red', 'orange', 'yellow', 'green', 'blue', 'cyan', 'black']
        
        # Create timeline
        y_pos = 0
        
        for i, (time, event, color) in enumerate(zip(times, events, colors)):
            ax.scatter([time], [y_pos], s=200, c=color, zorder=5)
            ax.text(time, y_pos + 0.1, event, ha='center', va='bottom', 
                   fontsize=10, rotation=45)
            
            # Draw connecting lines
            if i < len(times) - 1:
                ax.plot([time, times[i+1]], [y_pos, y_pos], 'k-', linewidth=2, alpha=0.5)
        
        # Highlight CMB
        cmb_idx = events.index('Recombination\n(CMB)')
        ax.scatter([times[cmb_idx]], [y_pos], s=400, facecolors='none', 
                  edgecolors='red', linewidth=3, zorder=6)
        
        ax.set_xscale('log')
        ax.set_xlim(1e-44, 2e10)
        ax.set_ylim(-0.3, 0.5)
        ax.set_xlabel('Time (years)')
        ax.set_title('Universe Timeline')
        ax.set_yticks([])
        
        # Add temperature scale
        ax2 = ax.twinx()
        
        # Temperature evolution (approximate)
        temperatures = np.array([1e32, 1e28, 1e15, 1e12, 1e9, 3000, 20, 2.7])  # Kelvin
        ax2.loglog(times, temperatures, 'r--', alpha=0.7, label='Temperature')
        ax2.set_ylabel('Temperature (K)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        
    def show(self):
        """Display all CMB visualizations."""
        self.plot_cmb_temperature_map(self.axes[0])
        self.plot_cmb_spectrum(self.axes[1])
        self.plot_universe_timeline(self.axes[2])
        
        plt.tight_layout()
        plt.show()


class StellarEvolution:
    """Visualize stellar evolution paths on HR diagram."""
    
    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        
    def plot_hr_diagram(self, ax):
        """Plot Hertzsprung-Russell diagram with evolutionary tracks."""
        # Temperature and luminosity ranges
        temperatures = np.logspace(np.log10(3000), np.log10(50000), 100)
        
        # Main sequence relationship (approximate)
        # L ∝ T^4 for main sequence stars
        main_sequence_luminosity = (temperatures / 5778)**4  # Relative to Sun
        
        ax.loglog(temperatures, main_sequence_luminosity, 'b-', linewidth=3, 
                 label='Main Sequence')
        
        # Giant branch
        giant_temps = np.linspace(3000, 5000, 50)
        giant_luminosities = np.logspace(1, 3, 50)
        ax.loglog(giant_temps, giant_luminosities, 'r-', linewidth=2, 
                 label='Red Giant Branch')
        
        # White dwarf cooling track
        wd_temps = np.logspace(np.log10(5000), np.log10(100000), 50)
        wd_luminosities = 10**(-(wd_temps/10000)**0.5)
        ax.loglog(wd_temps, wd_luminosities, 'w-', linewidth=2, 
                 markeredgecolor='black', label='White Dwarfs')
        
        # Add stellar types
        stellar_types = [
            (3500, 0.1, 'M'),
            (4000, 0.3, 'K'), 
            (5778, 1.0, 'G☉'),  # Sun
            (7000, 5, 'F'),
            (10000, 25, 'A'),
            (15000, 100, 'B'),
            (30000, 10000, 'O')
        ]
        
        for temp, lum, spec_type in stellar_types:
            ax.scatter([temp], [lum], s=100, c='yellow', edgecolors='black', zorder=5)
            ax.annotate(spec_type, (temp, lum), xytext=(10, 10), 
                       textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Evolutionary tracks for different masses
        masses = [1, 3, 10]  # Solar masses
        colors = ['green', 'orange', 'purple']
        
        for mass, color in zip(masses, colors):
            # Simplified evolutionary track
            if mass == 1:
                # Solar-type evolution
                track_temps = [5778, 5500, 4000, 3500, 20000]
                track_lums = [1, 1.5, 100, 1000, 0.01]
            elif mass == 3:
                # Intermediate mass
                track_temps = [7000, 6500, 4500, 30000]
                track_lums = [10, 15, 500, 0.1]
            else:  # mass == 10
                # High mass
                track_temps = [25000, 20000, 4000, 30000]
                track_lums = [5000, 8000, 50000, 1e-3]
                
            ax.loglog(track_temps, track_lums, 'o-', color=color, linewidth=2,
                     markersize=6, label=f'{mass} M☉ evolution')
        
        ax.set_xlabel('Surface Temperature (K)')
        ax.set_ylabel('Luminosity (L☉)')
        ax.set_title('Hertzsprung-Russell Diagram')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Invert x-axis (hotter stars on left)
        ax.invert_xaxis()
        
    def plot_stellar_lifecycle(self, ax):
        """Plot stellar lifecycle as a flowchart."""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        
        # Define stages and positions
        stages = [
            ('Nebula', 1, 8, 'lightblue'),
            ('Protostar', 3, 8, 'orange'),
            ('Main Sequence', 5, 8, 'yellow'),
            ('Red Giant', 7, 8, 'red'),
            ('Planetary Nebula', 8.5, 6, 'cyan'),
            ('White Dwarf', 8.5, 4, 'white'),
            ('Supernova', 7, 6, 'purple'),
            ('Neutron Star', 6, 4, 'gray'),
            ('Black Hole', 8, 4, 'black')
        ]
        
        # Draw stages
        for stage, x, y, color in stages:
            circle = Circle((x, y), 0.4, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, stage, ha='center', va='center', fontsize=8, 
                   fontweight='bold', wrap=True)
        
        # Draw evolution paths
        # Low mass path
        low_mass_path = [(1, 8), (3, 8), (5, 8), (7, 8), (8.5, 6), (8.5, 4)]
        for i in range(len(low_mass_path) - 1):
            x1, y1 = low_mass_path[i]
            x2, y2 = low_mass_path[i + 1]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        # High mass path
        high_mass_path = [(1, 8), (3, 8), (5, 8), (7, 8), (7, 6), (6, 4)]
        for i in range(len(high_mass_path) - 1):
            if i < 3:  # Skip common path
                continue
            x1, y1 = high_mass_path[i]
            x2, y2 = high_mass_path[i + 1]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        
        # Very high mass to black hole
        ax.annotate('', xy=(8, 4), xytext=(7, 6),
                   arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
        
        # Add mass labels
        ax.text(2, 6.5, 'Low Mass\n(< 8 M☉)', ha='center', fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax.text(6, 5.5, 'High Mass\n(8-25 M☉)', ha='center', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        ax.text(8.5, 5, 'Very High Mass\n(>25 M☉)', ha='center', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="plum"))
        
        ax.set_title('Stellar Evolution Pathways')
        ax.set_xticks([])
        ax.set_yticks([])
        
    def show(self):
        """Display stellar evolution visualizations."""
        self.plot_hr_diagram(self.axes[0])
        self.plot_stellar_lifecycle(self.axes[1])
        
        plt.tight_layout()
        plt.show()


def create_galaxy_collision_demo():
    """Interactive demo of galaxy collision dynamics."""
    plot = InteractivePhysicsPlot(figsize=(12, 8))
    
    # Parameters
    params = {
        'galaxy1_mass': 1e12,    # Solar masses
        'galaxy2_mass': 5e11,
        'approach_velocity': 200, # km/s
        'impact_parameter': 50    # kpc
    }
    
    def update_collision(val=None):
        """Update galaxy collision simulation."""
        plot.main_ax.clear()
        
        # Simple N-body simulation for galaxy collision
        # This is a very simplified model
        
        # Time evolution
        times = np.linspace(0, 2, 100)  # Gyr
        
        # Galaxy 1 trajectory (initially at rest)
        x1 = np.zeros_like(times)
        y1 = np.zeros_like(times)
        
        # Galaxy 2 trajectory (approaching)
        v_approach = params['approach_velocity']  # km/s
        impact_param = params['impact_parameter']  # kpc
        
        x2 = -200 + v_approach * times * 1e6 / 3.086e16  # Convert to kpc
        y2 = np.full_like(times, impact_param)
        
        # Gravitational interaction (simplified)
        G = 4.3e-3  # pc * (km/s)^2 / M_sun
        M1 = params['galaxy1_mass']
        M2 = params['galaxy2_mass']
        
        for i in range(1, len(times)):
            # Distance between galaxies
            dx = x2[i-1] - x1[i-1]
            dy = y2[i-1] - y1[i-1]
            r = np.sqrt(dx**2 + dy**2)
            
            if r > 1:  # Avoid singularities
                # Gravitational force
                F = G * M1 * M2 / r**2
                
                # Accelerations
                ax1 = F * dx / (r * M1)
                ay1 = F * dy / (r * M1)
                ax2 = -F * dx / (r * M2)
                ay2 = -F * dy / (r * M2)
                
                # Update positions (simplified integration)
                dt = times[i] - times[i-1]
                x1[i] = x1[i-1] + ax1 * dt**2
                y1[i] = y1[i-1] + ay1 * dt**2
                x2[i] = x2[i-1] + v_approach * dt + ax2 * dt**2
                y2[i] = y2[i-1] + ay2 * dt**2
            else:
                # Collision/merger
                x1[i] = x1[i-1]
                y1[i] = y1[i-1]
                x2[i] = x1[i]
                y2[i] = y1[i]
        
        # Plot galaxy trajectories
        plot.main_ax.plot(x1, y1, 'b-', linewidth=3, label=f'Galaxy 1 ({M1:.1e} M☉)')
        plot.main_ax.plot(x2, y2, 'r-', linewidth=3, label=f'Galaxy 2 ({M2:.1e} M☉)')
        
        # Show current positions
        plot.main_ax.scatter([x1[-1]], [y1[-1]], s=200, c='blue', marker='o', zorder=5)
        plot.main_ax.scatter([x2[-1]], [y2[-1]], s=150, c='red', marker='o', zorder=5)
        
        # Add tidal tails (simplified)
        if np.min(np.sqrt((x2-x1)**2 + (y2-y1)**2)) < 30:  # Close approach
            # Simple tidal tail representation
            for i in range(3):
                tail_length = 20 + i * 10
                angle = np.pi/4 + i * np.pi/6
                
                # Galaxy 1 tails
                tail_x1 = x1[-1] + tail_length * np.cos(angle)
                tail_y1 = y1[-1] + tail_length * np.sin(angle)
                plot.main_ax.plot([x1[-1], tail_x1], [y1[-1], tail_y1], 
                                 'b--', alpha=0.5, linewidth=2)
                
                # Galaxy 2 tails
                tail_x2 = x2[-1] - tail_length * np.cos(angle)
                tail_y2 = y2[-1] - tail_length * np.sin(angle)
                plot.main_ax.plot([x2[-1], tail_x2], [y2[-1], tail_y2], 
                                 'r--', alpha=0.5, linewidth=2)
        
        plot.main_ax.set_xlim(-250, 100)
        plot.main_ax.set_ylim(-50, 150)
        plot.main_ax.set_aspect('equal')
        plot.main_ax.set_xlabel('Distance (kpc)')
        plot.main_ax.set_ylabel('Distance (kpc)')
        plot.main_ax.set_title('Galaxy Collision Simulation')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add controls
    plot.add_slider('M1 (1e12)', 0.1, 3.0, params['galaxy1_mass']/1e12,
                   lambda val: (params.update({'galaxy1_mass': val*1e12}), update_collision()))
    plot.add_slider('M2 (1e11)', 1, 10, params['galaxy2_mass']/1e11,
                   lambda val: (params.update({'galaxy2_mass': val*1e11}), update_collision()))
    plot.add_slider('Velocity', 50, 500, params['approach_velocity'],
                   lambda val: (params.update({'approach_velocity': val}), update_collision()))
    
    # Initial plot
    update_collision()
    
    return plot


# Convenience functions for quick demonstrations
def demo_cosmic_expansion():
    """Quick cosmic expansion demo."""
    sim = CosmicExpansion(n_galaxies=30, hubble_constant=70)
    sim.start_animation(interval=100, frames=300)
    sim.show()

def demo_black_hole_accretion():
    """Quick black hole accretion demo."""
    sim = BlackHoleAccretion(black_hole_mass=10)
    sim.start_animation(interval=50, frames=500)
    sim.show()

def demo_cmb():
    """Quick cosmic microwave background demo."""
    cmb = CosmicMicrowaveBackground()
    cmb.show()

def demo_stellar_evolution():
    """Quick stellar evolution demo."""
    stellar = StellarEvolution()
    stellar.show()

def demo_galaxy_collision():
    """Quick galaxy collision demo."""
    demo = create_galaxy_collision_demo()
    demo.show()