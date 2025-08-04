"""Visual simulations for electromagnetic concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Optional, Callable
from ..visualization import (PhysicsAnimation, VectorField, ParticleTracker, 
                           setup_physics_plot, ColorMaps, create_3d_axes, InteractivePhysicsPlot)
from . import fields, lorentz, maxwell


class ElectricFieldVisualization:
    """Visualize electric fields from various charge configurations."""
    
    def __init__(self, figsize=(12, 10)):
        self.fig, self.axes = plt.subplots(2, 2, figsize=figsize)
        self.axes = self.axes.flatten()
        
    def plot_point_charge_field(self, ax, charge: float = 1e-9, position: Tuple[float, float] = (0, 0)):
        """Plot electric field lines for a point charge."""
        x_range = (-3, 3)
        y_range = (-3, 3)
        
        def electric_field(X, Y):
            """Calculate electric field at positions (X, Y)."""
            dx = X - position[0]
            dy = Y - position[1]
            r = np.sqrt(dx**2 + dy**2)
            
            # Avoid singularity at charge location
            r = np.maximum(r, 0.1)
            
            k = 8.99e9  # Coulomb's constant
            E_magnitude = k * abs(charge) / r**2
            
            if charge > 0:
                Ex = E_magnitude * dx / r
                Ey = E_magnitude * dy / r
            else:
                Ex = -E_magnitude * dx / r
                Ey = -E_magnitude * dy / r
                
            return Ex, Ey
            
        # Plot field lines using streamlines
        VectorField.plot_streamlines(ax, x_range, y_range, electric_field, 
                                    density=40, color='blue')
        
        # Plot charge
        color = 'red' if charge > 0 else 'blue'
        ax.scatter(*position, s=200, c=color, marker='o', edgecolors='black', linewidth=2)
        ax.text(position[0], position[1]+0.3, f'{charge*1e9:.1f} nC', 
               ha='center', fontsize=10, weight='bold')
        
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_aspect('equal')
        ax.set_title(f'Electric Field: Point Charge ({charge*1e9:.1f} nC)')
        ax.grid(True, alpha=0.3)
        
    def plot_dipole_field(self, ax, charge: float = 1e-9, separation: float = 1.0):
        """Plot electric field for an electric dipole."""
        pos1 = (-separation/2, 0)
        pos2 = (separation/2, 0)
        
        x_range = (-3, 3)
        y_range = (-2, 2)
        
        def dipole_field(X, Y):
            """Calculate dipole electric field."""
            # Field from positive charge
            dx1 = X - pos1[0]
            dy1 = Y - pos1[1]
            r1 = np.sqrt(dx1**2 + dy1**2)
            r1 = np.maximum(r1, 0.1)
            
            # Field from negative charge
            dx2 = X - pos2[0]
            dy2 = Y - pos2[1]
            r2 = np.sqrt(dx2**2 + dy2**2)
            r2 = np.maximum(r2, 0.1)
            
            k = 8.99e9
            E1_mag = k * charge / r1**2
            E2_mag = k * charge / r2**2
            
            # Superposition of fields
            Ex = E1_mag * dx1/r1 - E2_mag * dx2/r2
            Ey = E1_mag * dy1/r1 - E2_mag * dy2/r2
            
            return Ex, Ey
            
        VectorField.plot_streamlines(ax, x_range, y_range, dipole_field, 
                                    density=30, color='purple')
        
        # Plot charges
        ax.scatter(*pos1, s=200, c='red', marker='o', edgecolors='black', linewidth=2)
        ax.scatter(*pos2, s=200, c='blue', marker='o', edgecolors='black', linewidth=2)
        ax.text(pos1[0], pos1[1]+0.3, '+', ha='center', fontsize=16, weight='bold')
        ax.text(pos2[0], pos2[1]+0.3, '−', ha='center', fontsize=16, weight='bold')
        
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_aspect('equal')
        ax.set_title('Electric Field: Dipole')
        ax.grid(True, alpha=0.3)
        
    def plot_parallel_plates(self, ax, voltage: float = 100, separation: float = 2.0):
        """Plot uniform electric field between parallel plates."""
        x_range = (-3, 3)
        y_range = (-2, 2)
        
        def uniform_field(X, Y):
            """Uniform field between plates."""
            E_magnitude = voltage / separation
            # Field points from positive to negative plate
            Ex = np.zeros_like(X)
            Ey = -E_magnitude * np.ones_like(Y)
            
            # Only between plates
            mask = (Y > -separation/2) & (Y < separation/2)
            Ey = np.where(mask, Ey, 0)
            
            return Ex, Ey
            
        VectorField.plot_2d_field(ax, x_range, y_range, uniform_field, 
                                 density=15, scale=1e-3, color='green')
        
        # Draw plates
        plate_width = 4
        # Top plate (positive)
        ax.add_patch(plt.Rectangle((-plate_width/2, separation/2), plate_width, 0.1, 
                                  facecolor='red', edgecolor='black'))
        # Bottom plate (negative)  
        ax.add_patch(plt.Rectangle((-plate_width/2, -separation/2-0.1), plate_width, 0.1, 
                                  facecolor='blue', edgecolor='black'))
        
        # Labels
        ax.text(0, separation/2 + 0.3, f'+{voltage}V', ha='center', fontsize=12, weight='bold')
        ax.text(0, -separation/2 - 0.3, '0V', ha='center', fontsize=12, weight='bold')
        
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_aspect('equal')
        ax.set_title(f'Uniform Electric Field ({voltage}V, {separation}m separation)')
        ax.grid(True, alpha=0.3)
        
    def plot_field_superposition(self, ax):
        """Plot superposition of multiple charges."""
        charges = [
            (1e-9, (-1, 1)),    # +1 nC at (-1, 1)
            (-1e-9, (1, 1)),    # -1 nC at (1, 1)
            (2e-9, (0, -1))     # +2 nC at (0, -1)
        ]
        
        x_range = (-3, 3)
        y_range = (-3, 3)
        
        def superposition_field(X, Y):
            """Calculate superposition of all charge fields."""
            Ex_total = np.zeros_like(X)
            Ey_total = np.zeros_like(Y)
            
            k = 8.99e9
            
            for charge, pos in charges:
                dx = X - pos[0]
                dy = Y - pos[1]
                r = np.sqrt(dx**2 + dy**2)
                r = np.maximum(r, 0.1)
                
                E_mag = k * abs(charge) / r**2
                
                if charge > 0:
                    Ex_total += E_mag * dx / r
                    Ey_total += E_mag * dy / r
                else:
                    Ex_total -= E_mag * dx / r
                    Ey_total -= E_mag * dy / r
                    
            return Ex_total, Ey_total
            
        VectorField.plot_streamlines(ax, x_range, y_range, superposition_field, 
                                    density=35, color='orange')
        
        # Plot all charges
        for charge, pos in charges:
            color = 'red' if charge > 0 else 'blue'
            size = 150 + 50 * abs(charge * 1e9)  # Size proportional to charge
            ax.scatter(*pos, s=size, c=color, marker='o', edgecolors='black', linewidth=2)
            ax.text(pos[0], pos[1]+0.2, f'{charge*1e9:.1f}', ha='center', fontsize=9, weight='bold')
            
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.set_aspect('equal')
        ax.set_title('Electric Field: Superposition of Multiple Charges')
        ax.grid(True, alpha=0.3)
        
    def show(self):
        """Display all electric field visualizations."""
        self.plot_point_charge_field(self.axes[0], charge=2e-9)
        self.plot_dipole_field(self.axes[1], charge=1e-9, separation=1.2)
        self.plot_parallel_plates(self.axes[2], voltage=150, separation=1.5)
        self.plot_field_superposition(self.axes[3])
        
        plt.tight_layout()
        plt.show()


class ChargedParticleMotion(PhysicsAnimation):
    """Animate charged particles in electromagnetic fields."""
    
    def __init__(self, field_type: str = 'uniform_E', figsize=(10, 8)):
        super().__init__(figsize)
        self.field_type = field_type
        self.dt = 1e-3
        
        # Particle properties
        self.charge = 1.6e-19  # Elementary charge
        self.mass = 9.11e-31   # Electron mass
        
        # Initial conditions
        self.position = np.array([-3.0, 0.0])
        self.velocity = np.array([1e6, 0.5e6])  # m/s
        
        # Field parameters
        self.setup_field()
        
        # Trajectory tracking
        self.trajectory = [self.position.copy()]
        
        # Visualization elements
        self.particle_dot, = self.ax.plot([], [], 'ro', markersize=8, animated=True)
        self.trajectory_line, = self.ax.plot([], [], 'b-', alpha=0.7, linewidth=2, animated=True)
        self.velocity_arrow = None
        
        self.setup_plot()
        
    def setup_field(self):
        """Configure the electromagnetic field."""
        if self.field_type == 'uniform_E':
            self.E_field = np.array([0, 1e4])  # Uniform electric field
            self.B_field = np.array([0, 0, 0])
            
        elif self.field_type == 'uniform_B':
            self.E_field = np.array([0, 0])
            self.B_field = np.array([0, 0, 0.1])  # Uniform magnetic field
            
        elif self.field_type == 'crossed_EB':
            self.E_field = np.array([0, 1e4])
            self.B_field = np.array([0, 0, 0.05])
            
        elif self.field_type == 'cyclotron':
            self.E_field = np.array([0, 0])
            self.B_field = np.array([0, 0, 0.2])
            # Circular initial conditions
            self.position = np.array([0.0, -1.0])
            self.velocity = np.array([2e6, 0.0])
            
    def setup_plot(self):
        """Configure plot appearance."""
        self.ax.set_xlim(-4, 4)
        self.ax.set_ylim(-4, 4)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        self.ax.grid(True, alpha=0.3)
        
        # Add field visualization
        if self.field_type == 'uniform_E':
            self.ax.set_title('Charged Particle in Uniform Electric Field')
            # Draw field lines
            for x in np.linspace(-3, 3, 7):
                self.ax.arrow(x, -3, 0, 6, head_width=0.1, head_length=0.1, 
                             fc='green', ec='green', alpha=0.5)
                             
        elif self.field_type == 'uniform_B':
            self.ax.set_title('Charged Particle in Uniform Magnetic Field')
            # Draw B field symbols
            for x in range(-3, 4):
                for y in range(-3, 4):
                    self.ax.plot(x, y, 'x', color='red', markersize=8, alpha=0.5)
                    
        elif self.field_type == 'crossed_EB':
            self.ax.set_title('Charged Particle in Crossed E and B Fields')
            
        elif self.field_type == 'cyclotron':
            self.ax.set_title('Cyclotron Motion')
            
    def calculate_force(self, position: np.ndarray, velocity: np.ndarray) -> np.ndarray:
        """Calculate Lorentz force on the particle."""
        # F = q(E + v × B)
        E_force = self.charge * self.E_field
        
        # For 2D motion, v × B calculation
        v_cross_B = np.array([
            velocity[1] * self.B_field[2],  # v_y * B_z
            -velocity[0] * self.B_field[2], # -v_x * B_z
        ])
        
        B_force = self.charge * v_cross_B
        
        return E_force + B_force
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.position = np.array([-3.0, 0.0])
        if self.field_type == 'cyclotron':
            self.position = np.array([0.0, -1.0])
            self.velocity = np.array([2e6, 0.0])
        else:
            self.velocity = np.array([1e6, 0.5e6])
            
        self.trajectory = [self.position.copy()]
        
        return [self.particle_dot, self.trajectory_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Calculate force
        force = self.calculate_force(self.position, self.velocity)
        
        # Update velocity (F = ma)
        acceleration = force / self.mass
        self.velocity += acceleration * self.dt
        
        # Update position
        self.position += self.velocity * self.dt
        
        # Store trajectory
        self.trajectory.append(self.position.copy())
        
        # Limit trajectory length
        if len(self.trajectory) > 1000:
            self.trajectory.pop(0)
            
        # Update visualization
        self.particle_dot.set_data([self.position[0]], [self.position[1]])
        
        if len(self.trajectory) > 1:
            traj_array = np.array(self.trajectory)
            self.trajectory_line.set_data(traj_array[:, 0], traj_array[:, 1])
            
        return [self.particle_dot, self.trajectory_line]


class ElectromagneticWave(PhysicsAnimation):
    """Visualize electromagnetic wave propagation."""
    
    def __init__(self, wavelength: float = 2.0, amplitude: float = 1.0, figsize=(12, 8)):
        super().__init__(figsize)
        self.wavelength = wavelength
        self.amplitude = amplitude
        self.frequency = 3e8 / wavelength  # c = λf
        self.omega = 2 * np.pi * self.frequency
        self.k = 2 * np.pi / wavelength
        
        # Spatial grid
        self.x = np.linspace(0, 10, 200)
        
        # Plot elements for E and B fields
        self.E_line, = self.ax.plot([], [], 'b-', linewidth=3, label='Electric Field')
        self.B_line, = self.ax.plot([], [], 'r-', linewidth=3, label='Magnetic Field')
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-2*self.amplitude, 2*self.amplitude)
        self.ax.set_xlabel('Position (m)')
        self.ax.set_ylabel('Field Amplitude')
        self.ax.set_title(f'Electromagnetic Wave (λ={self.wavelength}m, f={self.frequency:.2e}Hz)')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        # Add zero line
        self.ax.axhline(0, color='black', linewidth=0.5, alpha=0.5)
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.E_line, self.B_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * 0.01  # Time step
        
        # Wave equations
        # E(x,t) = A sin(kx - ωt)
        # B(x,t) = (A/c) sin(kx - ωt)
        
        E_field = self.amplitude * np.sin(self.k * self.x - self.omega * t)
        B_field = (self.amplitude / 3e8) * np.sin(self.k * self.x - self.omega * t) * 1e8  # Scaled for visibility
        
        self.E_line.set_data(self.x, E_field)
        self.B_line.set_data(self.x, B_field)
        
        return [self.E_line, self.B_line]


class ElectromagneticWave3D:
    """3D visualization of electromagnetic wave."""
    
    def __init__(self, figsize=(12, 9)):
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Wave parameters
        self.wavelength = 2.0
        self.k = 2 * np.pi / self.wavelength
        self.omega = 3e8 * self.k
        
        # Spatial grid
        self.z = np.linspace(0, 8, 100)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure 3D plot."""
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.set_zlim(0, 8)
        self.ax.set_xlabel('X (E-field direction)')
        self.ax.set_ylabel('Y (B-field direction)')
        self.ax.set_zlabel('Z (Propagation direction)')
        self.ax.set_title('3D Electromagnetic Wave')
        
    def animate_wave(self, t: float = 0):
        """Plot EM wave at time t."""
        self.ax.clear()
        self.setup_plot()
        
        # Calculate field values
        E_field = np.sin(self.k * self.z - self.omega * t)
        B_field = np.sin(self.k * self.z - self.omega * t)
        
        # Plot E field (oscillating in x direction)
        self.ax.plot(E_field, np.zeros_like(self.z), self.z, 'b-', linewidth=3, label='E-field')
        
        # Plot B field (oscillating in y direction)
        self.ax.plot(np.zeros_like(self.z), B_field, self.z, 'r-', linewidth=3, label='B-field')
        
        # Add field vectors at several points
        n_vectors = 8
        indices = np.linspace(0, len(self.z)-1, n_vectors, dtype=int)
        
        for i in indices[::2]:  # Every other vector for clarity
            z_pos = self.z[i]
            E_val = E_field[i]
            B_val = B_field[i]
            
            if abs(E_val) > 0.1:  # Only draw significant vectors
                # E field vector
                self.ax.quiver(0, 0, z_pos, E_val, 0, 0, color='blue', alpha=0.7, arrow_length_ratio=0.1)
                # B field vector
                self.ax.quiver(0, 0, z_pos, 0, B_val, 0, color='red', alpha=0.7, arrow_length_ratio=0.1)
                
        self.ax.legend()
        
    def show_static(self):
        """Show static 3D wave."""
        self.animate_wave(t=0)
        plt.show()


def create_lorentz_force_demo():
    """Interactive demo of Lorentz force on moving charges."""
    plot = InteractivePhysicsPlot(figsize=(12, 8))
    
    # Parameters
    params = {
        'E_magnitude': 1e4,
        'B_magnitude': 0.1,
        'particle_charge': 1.6e-19,
        'particle_mass': 9.11e-31
    }
    
    def update_simulation(val=None):
        """Update the Lorentz force simulation."""
        plot.main_ax.clear()
        
        # Create charged particle simulation
        sim = ChargedParticleMotion(field_type='crossed_EB')
        sim.E_field = np.array([0, params['E_magnitude']])
        sim.B_field = np.array([0, 0, params['B_magnitude']])
        sim.charge = params['particle_charge']
        sim.mass = params['particle_mass']
        
        # Run simulation for several steps
        positions = [sim.position.copy()]
        for _ in range(200):
            force = sim.calculate_force(sim.position, sim.velocity)
            acceleration = force / sim.mass
            sim.velocity += acceleration * sim.dt
            sim.position += sim.velocity * sim.dt
            positions.append(sim.position.copy())
            
        # Plot trajectory
        positions = np.array(positions)
        plot.main_ax.plot(positions[:, 0], positions[:, 1], 'b-', linewidth=2, label='Particle Path')
        plot.main_ax.scatter(positions[0, 0], positions[0, 1], c='green', s=100, label='Start', zorder=5)
        plot.main_ax.scatter(positions[-1, 0], positions[-1, 1], c='red', s=100, label='End', zorder=5)
        
        # Field visualization
        plot.main_ax.arrow(-3, -3, 0, 6, head_width=0.1, head_length=0.1, 
                          fc='orange', ec='orange', alpha=0.5, label='E-field')
        
        plot.main_ax.set_xlim(-4, 4)
        plot.main_ax.set_ylim(-4, 4)
        plot.main_ax.set_aspect('equal')
        plot.main_ax.set_title(f'Lorentz Force: q={params["particle_charge"]:.2e}C')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add controls
    plot.add_slider('E Field', 1e3, 1e5, params['E_magnitude'], 
                   lambda val: (params.update({'E_magnitude': val}), update_simulation()))
    plot.add_slider('B Field', 0.01, 0.5, params['B_magnitude'],
                   lambda val: (params.update({'B_magnitude': val}), update_simulation()))
    
    # Initial plot
    update_simulation()
    
    return plot


# Convenience functions for quick demonstrations
def demo_electric_fields():
    """Quick electric field visualization demo."""
    viz = ElectricFieldVisualization()
    viz.show()

def demo_particle_motion():
    """Quick charged particle motion demo."""
    sim = ChargedParticleMotion(field_type='cyclotron')
    sim.start_animation(interval=20, frames=1000)
    sim.show()

def demo_em_wave():
    """Quick electromagnetic wave demo."""
    sim = ElectromagneticWave(wavelength=3.0, amplitude=1.5)
    sim.start_animation(interval=50, frames=500)
    sim.show()

def demo_em_wave_3d():
    """Quick 3D electromagnetic wave demo."""
    viz = ElectromagneticWave3D()
    viz.show_static()

def demo_lorentz_force():
    """Quick Lorentz force demo."""
    demo = create_lorentz_force_demo()
    demo.show()