"""Visual simulations for waves and optics concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.collections import LineCollection
from typing import List, Tuple, Optional, Union
from ..visualization import PhysicsAnimation, setup_physics_plot, ColorMaps, InteractivePhysicsPlot
from . import wave_equation, interference, ray_tracing


class WaveInterferenceSimulation(PhysicsAnimation):
    """Simulate wave interference patterns from multiple sources."""
    
    def __init__(self, source_positions: List[Tuple[float, float]], 
                 wavelength: float = 1.0, amplitude: float = 1.0, figsize=(10, 8)):
        super().__init__(figsize)
        self.source_positions = source_positions
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.k = 2 * np.pi / wavelength
        self.omega = self.k  # Assume c = 1 for simplicity
        
        # Create spatial grid
        self.x = np.linspace(-5, 5, 200)
        self.y = np.linspace(-5, 5, 200)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Visualization
        self.im = self.ax.imshow(np.zeros_like(self.X), cmap=ColorMaps.WAVE_AMPLITUDE, 
                                vmin=-2*amplitude, vmax=2*amplitude, 
                                extent=[-5, 5, -5, 5], animated=True)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title(f'Wave Interference ({len(self.source_positions)} sources, λ={self.wavelength})')
        
        # Plot source positions
        for i, pos in enumerate(self.source_positions):
            self.ax.scatter(*pos, s=100, c='white', marker='o', edgecolors='black', 
                           linewidth=2, zorder=5, label=f'Source {i+1}' if i < 3 else '')
            
        if len(self.source_positions) <= 3:
            self.ax.legend()
            
        # Add colorbar
        cbar = plt.colorbar(self.im, ax=self.ax)
        cbar.set_label('Wave Amplitude', rotation=270, labelpad=15)
        
    def calculate_wave_field(self, t: float) -> np.ndarray:
        """Calculate wave field at time t."""
        field = np.zeros_like(self.X)
        
        for pos in self.source_positions:
            # Distance from each source
            dx = self.X - pos[0]
            dy = self.Y - pos[1]
            r = np.sqrt(dx**2 + dy**2)
            
            # Avoid singularity at source
            r = np.maximum(r, 0.1)
            
            # Circular wave from each source: A * sin(kr - ωt) / r
            wave = self.amplitude * np.sin(self.k * r - self.omega * t) / np.sqrt(r)
            field += wave
            
        return field
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.im]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * 0.1
        field = self.calculate_wave_field(t)
        self.im.set_array(field)
        return [self.im]


class DoubleSlitExperiment(PhysicsAnimation):
    """Simulate the famous double-slit experiment."""
    
    def __init__(self, slit_separation: float = 2.0, slit_width: float = 0.2, 
                 wavelength: float = 0.5, screen_distance: float = 10.0, figsize=(12, 8)):
        super().__init__(figsize)
        self.slit_separation = slit_separation
        self.slit_width = slit_width
        self.wavelength = wavelength
        self.screen_distance = screen_distance
        self.k = 2 * np.pi / wavelength
        
        # Create two subplot: wave propagation and intensity pattern
        self.fig.clear()
        self.ax_wave = self.fig.add_subplot(121)
        self.ax_pattern = self.fig.add_subplot(122)
        
        # Spatial grids
        self.x = np.linspace(-3, 15, 300)
        self.y = np.linspace(-5, 5, 200)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        # Wave visualization
        self.im = self.ax_wave.imshow(np.zeros_like(self.X), cmap=ColorMaps.WAVE_AMPLITUDE,
                                     vmin=-2, vmax=2, extent=[-3, 15, -5, 5], animated=True)
        
        # Intensity pattern
        self.intensity_line, = self.ax_pattern.plot([], [], 'r-', linewidth=2)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Wave propagation plot
        self.ax_wave.set_xlabel('x')
        self.ax_wave.set_ylabel('y')
        self.ax_wave.set_title('Wave Propagation Through Double Slit')
        
        # Draw the barrier with slits
        barrier_x = 5
        barrier_height = 10
        
        # Top part of barrier
        self.ax_wave.add_patch(Rectangle((barrier_x-0.1, self.slit_separation/2 + self.slit_width/2), 
                                        0.2, barrier_height, facecolor='black'))
        # Bottom part of barrier  
        self.ax_wave.add_patch(Rectangle((barrier_x-0.1, -barrier_height), 
                                        0.2, barrier_height - self.slit_separation/2 + self.slit_width/2, 
                                        facecolor='black'))
        # Middle part (between slits)
        self.ax_wave.add_patch(Rectangle((barrier_x-0.1, -self.slit_separation/2 + self.slit_width/2), 
                                        0.2, self.slit_separation - self.slit_width, facecolor='black'))
        
        # Draw screen
        self.ax_wave.axvline(x=self.screen_distance, color='gray', linewidth=3, alpha=0.7)
        
        # Intensity pattern plot
        self.ax_pattern.set_xlabel('y position on screen')
        self.ax_pattern.set_ylabel('Intensity')
        self.ax_pattern.set_title('Interference Pattern')
        self.ax_pattern.grid(True, alpha=0.3)
        
    def calculate_wave_field(self, t: float) -> np.ndarray:
        """Calculate wave field at time t."""
        # Incident plane wave from left
        incident_wave = np.sin(self.k * self.X - t)
        
        # Mask for the barrier (block wave except at slits)
        barrier_x = 5
        barrier_mask = np.abs(self.X - barrier_x) < 0.1
        
        # Slit positions
        slit1_y = self.slit_separation / 2
        slit2_y = -self.slit_separation / 2
        
        # Allow wave through slits
        slit1_mask = (barrier_mask & 
                     (np.abs(self.Y - slit1_y) < self.slit_width/2))
        slit2_mask = (barrier_mask & 
                     (np.abs(self.Y - slit2_y) < self.slit_width/2))
        
        # Block wave at barrier except at slits
        field = incident_wave.copy()
        field[barrier_mask & ~slit1_mask & ~slit2_mask] = 0
        
        # Beyond the barrier, calculate interference from the two slits
        beyond_barrier = self.X > barrier_x + 0.1
        
        if np.any(beyond_barrier):
            # Distance from each slit
            r1 = np.sqrt((self.X - barrier_x)**2 + (self.Y - slit1_y)**2)
            r2 = np.sqrt((self.X - barrier_x)**2 + (self.Y - slit2_y)**2)
            
            # Waves from each slit (with 1/r amplitude decay)
            wave1 = np.sin(self.k * r1 - t) / np.sqrt(r1 + 1)
            wave2 = np.sin(self.k * r2 - t) / np.sqrt(r2 + 1)
            
            # Superposition beyond barrier
            field[beyond_barrier] = wave1[beyond_barrier] + wave2[beyond_barrier]
            
        return field
        
    def calculate_screen_intensity(self, field: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate intensity pattern at the screen."""
        screen_idx = np.argmin(np.abs(self.x - self.screen_distance))
        screen_pattern = field[:, screen_idx]
        intensity = screen_pattern**2
        return self.y, intensity
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.im, self.intensity_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * 0.2
        field = self.calculate_wave_field(t)
        
        # Update wave field
        self.im.set_array(field)
        
        # Update intensity pattern
        y_screen, intensity = self.calculate_screen_intensity(field)
        self.intensity_line.set_data(intensity * 5, y_screen)  # Scale for visibility
        
        # Update intensity plot limits
        if frame == 0:
            self.ax_pattern.set_xlim(0, np.max(intensity) * 6)
            self.ax_pattern.set_ylim(-5, 5)
            
        return [self.im, self.intensity_line]


class ReflectionRefractionDemo:
    """Demonstrate reflection and refraction using ray tracing."""
    
    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        
    def plot_reflection(self, ax, incident_angle: float = 30.0):
        """Plot ray reflection at an interface."""
        # Convert to radians
        theta_i = np.radians(incident_angle)
        
        # Interface at y = 0
        interface_x = np.linspace(-3, 3, 100)
        interface_y = np.zeros_like(interface_x)
        ax.plot(interface_x, interface_y, 'k-', linewidth=3, label='Interface')
        
        # Incident ray
        ray_length = 2
        incident_x = [0 - ray_length * np.sin(theta_i), 0]
        incident_y = [ray_length * np.cos(theta_i), 0]
        ax.plot(incident_x, incident_y, 'b-', linewidth=2, label='Incident Ray')
        
        # Reflected ray (angle of reflection = angle of incidence)
        theta_r = theta_i
        reflected_x = [0, ray_length * np.sin(theta_r)]
        reflected_y = [0, ray_length * np.cos(theta_r)]
        ax.plot(reflected_x, reflected_y, 'r-', linewidth=2, label='Reflected Ray')
        
        # Normal line
        ax.plot([0, 0], [-0.5, 2.5], 'k--', alpha=0.5, label='Normal')
        
        # Angle markers
        arc_radius = 0.5
        
        # Incident angle
        incident_arc = np.linspace(np.pi/2 - theta_i, np.pi/2, 50)
        ax.plot(arc_radius * np.cos(incident_arc), arc_radius * np.sin(incident_arc), 'b--', alpha=0.7)
        ax.text(-0.3, 0.6, f'θᵢ = {incident_angle}°', fontsize=10, color='blue')
        
        # Reflected angle
        reflected_arc = np.linspace(np.pi/2, np.pi/2 + theta_r, 50)
        ax.plot(arc_radius * np.cos(reflected_arc), arc_radius * np.sin(reflected_arc), 'r--', alpha=0.7)
        ax.text(0.1, 0.6, f'θᵣ = {incident_angle}°', fontsize=10, color='red')
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-1, 3)
        ax.set_aspect('equal')
        ax.set_title(f'Reflection (θᵢ = θᵣ = {incident_angle}°)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_refraction(self, ax, incident_angle: float = 30.0, n1: float = 1.0, n2: float = 1.5):
        """Plot ray refraction at an interface."""
        # Convert to radians
        theta_i = np.radians(incident_angle)
        
        # Calculate refracted angle using Snell's law: n1*sin(θ1) = n2*sin(θ2)
        sin_theta_t = (n1 / n2) * np.sin(theta_i)
        
        if sin_theta_t > 1:
            # Total internal reflection
            self.plot_total_internal_reflection(ax, incident_angle, n1, n2)
            return
            
        theta_t = np.arcsin(sin_theta_t)
        
        # Interface at y = 0
        interface_x = np.linspace(-3, 3, 100)
        interface_y = np.zeros_like(interface_x)
        ax.plot(interface_x, interface_y, 'k-', linewidth=3, label='Interface')
        
        # Medium labels
        ax.text(-2.5, 1.5, f'n₁ = {n1}', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax.text(-2.5, -1.5, f'n₂ = {n2}', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        
        # Incident ray
        ray_length = 2
        incident_x = [0 - ray_length * np.sin(theta_i), 0]
        incident_y = [ray_length * np.cos(theta_i), 0]
        ax.plot(incident_x, incident_y, 'b-', linewidth=2, label='Incident Ray')
        
        # Refracted ray
        refracted_x = [0, ray_length * np.sin(theta_t)]
        refracted_y = [0, -ray_length * np.cos(theta_t)]
        ax.plot(refracted_x, refracted_y, 'g-', linewidth=2, label='Refracted Ray')
        
        # Normal line
        ax.plot([0, 0], [-2.5, 2.5], 'k--', alpha=0.5, label='Normal')
        
        # Angle markers
        arc_radius = 0.5
        
        # Incident angle
        incident_arc = np.linspace(np.pi/2 - theta_i, np.pi/2, 50)
        ax.plot(arc_radius * np.cos(incident_arc), arc_radius * np.sin(incident_arc), 'b--', alpha=0.7)
        ax.text(-0.4, 0.6, f'θᵢ = {incident_angle}°', fontsize=10, color='blue')
        
        # Refracted angle
        refracted_arc = np.linspace(-np.pi/2, -np.pi/2 + theta_t, 50)
        ax.plot(arc_radius * np.cos(refracted_arc), arc_radius * np.sin(refracted_arc), 'g--', alpha=0.7)
        ax.text(0.1, -0.7, f'θₜ = {np.degrees(theta_t):.1f}°', fontsize=10, color='green')
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.set_title(f'Refraction (Snell\'s Law)\nn₁sin(θᵢ) = n₂sin(θₜ)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_total_internal_reflection(self, ax, incident_angle: float, n1: float, n2: float):
        """Plot total internal reflection when it occurs."""
        # Critical angle
        theta_c = np.degrees(np.arcsin(n2 / n1))
        
        theta_i = np.radians(incident_angle)
        
        # Interface
        interface_x = np.linspace(-3, 3, 100)
        ax.plot(interface_x, np.zeros_like(interface_x), 'k-', linewidth=3, label='Interface')
        
        # Medium labels
        ax.text(-2.5, 1.5, f'n₁ = {n1}', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        ax.text(-2.5, -1.5, f'n₂ = {n2}', fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        
        # Incident ray
        ray_length = 2
        incident_x = [0 - ray_length * np.sin(theta_i), 0]
        incident_y = [ray_length * np.cos(theta_i), 0]
        ax.plot(incident_x, incident_y, 'b-', linewidth=2, label='Incident Ray')
        
        # Totally reflected ray
        reflected_x = [0, ray_length * np.sin(theta_i)]
        reflected_y = [0, ray_length * np.cos(theta_i)]
        ax.plot(reflected_x, reflected_y, 'r-', linewidth=2, label='Totally Reflected Ray')
        
        # Normal line
        ax.plot([0, 0], [-2.5, 2.5], 'k--', alpha=0.5, label='Normal')
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.set_title(f'Total Internal Reflection\nθᵢ = {incident_angle}° > θc = {theta_c:.1f}°')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def show(self, incident_angle: float = 30.0, n1: float = 1.0, n2: float = 1.5):
        """Display reflection and refraction demonstrations."""
        self.plot_reflection(self.axes[0], incident_angle)
        self.plot_refraction(self.axes[1], incident_angle, n1, n2)
        
        plt.tight_layout()
        plt.show()


class DiffractionSimulation(PhysicsAnimation):
    """Simulate single-slit diffraction pattern."""
    
    def __init__(self, slit_width: float = 2.0, wavelength: float = 0.5, 
                 screen_distance: float = 10.0, figsize=(12, 6)):
        super().__init__(figsize)
        self.slit_width = slit_width
        self.wavelength = wavelength
        self.screen_distance = screen_distance
        self.k = 2 * np.pi / wavelength
        
        # Create subplots
        self.fig.clear()
        self.ax_diffraction = self.fig.add_subplot(121)
        self.ax_pattern = self.fig.add_subplot(122)
        
        # Spatial grid
        self.y_screen = np.linspace(-5, 5, 300)
        
        # Pattern line
        self.pattern_line, = self.ax_pattern.plot([], [], 'r-', linewidth=2)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Diffraction geometry
        self.ax_diffraction.set_xlim(-2, 12)
        self.ax_diffraction.set_ylim(-4, 4)
        self.ax_diffraction.set_aspect('equal')
        self.ax_diffraction.set_title('Single-Slit Diffraction Geometry')
        
        # Draw slit
        slit_x = 0
        barrier_height = 8
        # Top part of barrier
        self.ax_diffraction.add_patch(Rectangle((slit_x-0.1, self.slit_width/2), 
                                               0.2, barrier_height, facecolor='black'))
        # Bottom part of barrier
        self.ax_diffraction.add_patch(Rectangle((slit_x-0.1, -barrier_height), 
                                               0.2, barrier_height - self.slit_width/2, facecolor='black'))
        
        # Draw screen
        self.ax_diffraction.axvline(x=self.screen_distance, color='gray', linewidth=3, alpha=0.7)
        
        # Add some ray paths
        for y_slit in np.linspace(-self.slit_width/2, self.slit_width/2, 5):
            for y_screen in [-2, 0, 2]:
                self.ax_diffraction.plot([0, self.screen_distance], [y_slit, y_screen], 
                                        'b--', alpha=0.3, linewidth=1)
        
        self.ax_diffraction.set_xlabel('Distance (m)')
        self.ax_diffraction.set_ylabel('y (m)')
        
        # Diffraction pattern
        self.ax_pattern.set_xlabel('Intensity')
        self.ax_pattern.set_ylabel('y position on screen (m)')
        self.ax_pattern.set_title('Diffraction Pattern')
        self.ax_pattern.grid(True, alpha=0.3)
        
    def calculate_diffraction_pattern(self) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate single-slit diffraction pattern using Fraunhofer approximation."""
        # Angle from slit center to screen position
        theta = np.arctan(self.y_screen / self.screen_distance)
        
        # Diffraction parameter
        beta = (np.pi * self.slit_width * np.sin(theta)) / self.wavelength
        
        # Avoid division by zero
        beta = np.where(np.abs(beta) < 1e-10, 1e-10, beta)
        
        # Single-slit diffraction intensity: I = I₀ * (sin(β)/β)²
        intensity = (np.sin(beta) / beta)**2
        
        return self.y_screen, intensity
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.pattern_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame (static pattern for single-slit)."""
        y_pos, intensity = self.calculate_diffraction_pattern()
        self.pattern_line.set_data(intensity, y_pos)
        
        # Set limits based on pattern
        if frame == 0:
            self.ax_pattern.set_xlim(0, 1.1)
            self.ax_pattern.set_ylim(-5, 5)
            
        return [self.pattern_line]


def create_wave_superposition_demo():
    """Interactive demo of wave superposition."""
    plot = InteractivePhysicsPlot(figsize=(12, 8))
    
    # Parameters
    params = {
        'amplitude1': 1.0,
        'frequency1': 1.0,
        'amplitude2': 0.8,
        'frequency2': 1.2,
        'phase_diff': 0.0
    }
    
    def update_waves(val=None):
        """Update wave superposition plot."""
        plot.main_ax.clear()
        
        # Spatial and time arrays
        x = np.linspace(0, 10, 500)
        t = 0  # Static snapshot
        
        # Individual waves
        wave1 = params['amplitude1'] * np.sin(2*np.pi*params['frequency1']*x/5 + params['phase_diff'])
        wave2 = params['amplitude2'] * np.sin(2*np.pi*params['frequency2']*x/5)
        superposition = wave1 + wave2
        
        # Plot waves
        plot.main_ax.plot(x, wave1, 'b-', linewidth=2, alpha=0.7, label=f'Wave 1 (A={params["amplitude1"]:.1f}, f={params["frequency1"]:.1f})')
        plot.main_ax.plot(x, wave2, 'r-', linewidth=2, alpha=0.7, label=f'Wave 2 (A={params["amplitude2"]:.1f}, f={params["frequency2"]:.1f})')
        plot.main_ax.plot(x, superposition, 'k-', linewidth=3, label='Superposition')
        
        plot.main_ax.set_xlim(0, 10)
        plot.main_ax.set_ylim(-3, 3)
        plot.main_ax.set_xlabel('Position')
        plot.main_ax.set_ylabel('Amplitude')
        plot.main_ax.set_title('Wave Superposition')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add controls
    plot.add_slider('Amp 1', 0.1, 2.0, params['amplitude1'], 
                   lambda val: (params.update({'amplitude1': val}), update_waves()))
    plot.add_slider('Freq 1', 0.5, 3.0, params['frequency1'],
                   lambda val: (params.update({'frequency1': val}), update_waves()))
    plot.add_slider('Amp 2', 0.1, 2.0, params['amplitude2'],
                   lambda val: (params.update({'amplitude2': val}), update_waves()))
    plot.add_slider('Freq 2', 0.5, 3.0, params['frequency2'],
                   lambda val: (params.update({'frequency2': val}), update_waves()))
    
    # Initial plot
    update_waves()
    
    return plot


# Convenience functions for quick demonstrations
def demo_wave_interference():
    """Quick wave interference demo."""
    sources = [(0, 2), (0, -2)]  # Two sources
    sim = WaveInterferenceSimulation(sources, wavelength=1.0)
    sim.start_animation(interval=50, frames=200)
    sim.show()

def demo_double_slit():
    """Quick double-slit experiment demo."""
    sim = DoubleSlitExperiment(slit_separation=1.5, wavelength=0.4)
    sim.start_animation(interval=100, frames=100)
    sim.show()

def demo_reflection_refraction():
    """Quick reflection and refraction demo."""
    demo = ReflectionRefractionDemo()
    demo.show(incident_angle=45, n1=1.0, n2=1.5)

def demo_diffraction():
    """Quick single-slit diffraction demo."""
    sim = DiffractionSimulation(slit_width=2.0, wavelength=0.6)
    sim.start_animation(interval=100, frames=50)  # Static pattern
    sim.show()

def demo_wave_superposition():
    """Quick wave superposition demo."""
    demo = create_wave_superposition_demo()
    demo.show()