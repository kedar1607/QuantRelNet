"""Visual simulations for relativity concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Optional, Callable
from ..visualization import PhysicsAnimation, setup_physics_plot, create_3d_axes, InteractivePhysicsPlot
from . import special, general


class SpacetimeDiagram:
    """Create Minkowski spacetime diagrams for special relativity."""
    
    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        self.c = 299792458  # Speed of light (m/s)
        
    def plot_time_dilation(self, ax, velocity: float = 0.6):
        """Plot spacetime diagram showing time dilation."""
        # Convert velocity to fraction of c
        beta = velocity
        gamma = 1 / np.sqrt(1 - beta**2)
        
        # Time and space coordinates
        t = np.linspace(0, 5, 100)
        x = np.linspace(-3, 3, 100)
        
        # Rest frame (stationary observer)
        ax.axhline(0, color='black', linewidth=1, alpha=0.5)
        ax.axvline(0, color='black', linewidth=1, alpha=0.5)
        
        # Light cone
        ax.plot(t, t, 'gray', linestyle='--', alpha=0.7, label='Light cone')
        ax.plot(t, -t, 'gray', linestyle='--', alpha=0.7)
        
        # Stationary observer worldline
        ax.plot([0]*len(t), t, 'b-', linewidth=3, label='Stationary observer')
        
        # Moving observer worldline
        moving_x = beta * t
        ax.plot(moving_x, t, 'r-', linewidth=3, label=f'Moving observer (v={beta:.1f}c)')
        
        # Simultaneity lines for moving observer
        for t_event in [1, 2, 3, 4]:
            # Line of simultaneity has slope 1/(β*γ²)
            slope = 1/(beta * gamma**2) if beta != 0 else np.inf
            if slope != np.inf:
                x_simul = np.linspace(-2, 2, 50)
                t_simul = t_event + slope * (x_simul - beta * t_event)
                ax.plot(x_simul, t_simul, 'r--', alpha=0.5, linewidth=1)
        
        # Mark time intervals
        for i, t_mark in enumerate([1, 2, 3]):
            # Proper time interval for moving observer
            ax.plot([beta * t_mark], [t_mark], 'ro', markersize=8)
            ax.annotate(f'τ={t_mark/gamma:.1f}', 
                       xy=(beta * t_mark, t_mark), xytext=(10, 10),
                       textcoords='offset points', fontsize=10, color='red')
            
            # Coordinate time interval for stationary observer  
            ax.plot([0], [t_mark], 'bo', markersize=8)
            ax.annotate(f't={t_mark}', 
                       xy=(0, t_mark), xytext=(-30, 10),
                       textcoords='offset points', fontsize=10, color='blue')
        
        ax.set_xlim(-1, 4)
        ax.set_ylim(0, 5)
        ax.set_xlabel('Space (ct)')
        ax.set_ylabel('Time (ct)')
        ax.set_title(f'Time Dilation (γ={gamma:.2f})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_length_contraction(self, ax, velocity: float = 0.8):
        """Plot spacetime diagram showing length contraction."""
        beta = velocity
        gamma = 1 / np.sqrt(1 - beta**2)
        
        # Proper length of rod
        L0 = 2.0
        
        # Coordinate system
        ax.axhline(0, color='black', linewidth=1, alpha=0.5)
        ax.axvline(0, color='black', linewidth=1, alpha=0.5)
        
        # Light cone
        t_light = np.linspace(0, 4, 100)
        ax.plot(t_light, t_light, 'gray', linestyle='--', alpha=0.7)
        ax.plot(t_light, -t_light, 'gray', linestyle='--', alpha=0.7)
        
        # Rest frame rod (vertical worldlines)
        ax.plot([0, 0], [0, 4], 'b-', linewidth=3, label='Rod end A (rest)')
        ax.plot([L0, L0], [0, 4], 'b-', linewidth=3, label='Rod end B (rest)')
        
        # Fill rest frame rod
        ax.fill_betweenx([0, 4], 0, L0, alpha=0.2, color='blue')
        
        # Moving frame rod
        for t in [1, 2, 3]:
            # Worldlines of rod ends in moving frame
            xA_moving = beta * t
            xB_moving = beta * t + L0
            
            # Line of simultaneity in moving frame
            x_simul = np.linspace(-1, 5, 100)
            t_simul = t + (x_simul - beta * t) / (beta * gamma**2)
            
            # Find intersections with rod worldlines
            # For vertical worldlines, intersection is straightforward
            t_A = t
            t_B = t + L0 / (beta * gamma**2)
            
            if t_B <= 4:  # Only plot if within bounds
                ax.plot([0, L0], [t_A, t_B], 'r-', linewidth=2, alpha=0.7)
        
        # Show contracted length measurement
        t_measure = 2
        L_contracted = L0 / gamma
        ax.annotate('', xy=(L_contracted, t_measure), xytext=(0, t_measure),
                   arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax.text(L_contracted/2, t_measure+0.2, f'L = L₀/γ = {L_contracted:.1f}',
                ha='center', fontsize=10, color='red', 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        ax.set_xlim(-0.5, 3)
        ax.set_ylim(0, 4)
        ax.set_xlabel('Space (units of L₀)')
        ax.set_ylabel('Time (arbitrary units)')
        ax.set_title(f'Length Contraction (L₀={L0}, γ={gamma:.2f})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def show(self, v1: float = 0.6, v2: float = 0.8):
        """Display spacetime diagrams."""
        self.plot_time_dilation(self.axes[0], v1)
        self.plot_length_contraction(self.axes[1], v2)
        
        plt.tight_layout()
        plt.show()


class RelativisticMotion(PhysicsAnimation):
    """Animate relativistic particle motion and effects."""
    
    def __init__(self, scenario: str = 'acceleration', figsize=(12, 6)):
        super().__init__(figsize)
        self.scenario = scenario
        self.c = 1.0  # Set c = 1 for convenience
        self.dt = 0.01
        
        # Create subplots
        self.fig.clear()
        if scenario == 'acceleration':
            self.ax_motion = self.fig.add_subplot(121)
            self.ax_gamma = self.fig.add_subplot(122)
        else:
            self.ax_motion = self.fig.add_subplot(111)
            
        self.setup_scenario()
        self.setup_plot()
        
    def setup_scenario(self):
        """Set up the specific relativistic scenario."""
        if self.scenario == 'acceleration':
            # Particle undergoing constant proper acceleration
            self.proper_acceleration = 1.0  # units where c = 1
            self.initial_velocity = 0.0
            self.initial_position = 0.0
            
            # Storage for trajectory
            self.times = [0]
            self.positions = [self.initial_position]
            self.velocities = [self.initial_velocity]
            self.gammas = [1.0]
            
        elif self.scenario == 'twin_paradox':
            # Twin paradox setup
            self.travel_time = 5.0
            self.travel_velocity = 0.8
            self.gamma_travel = 1 / np.sqrt(1 - self.travel_velocity**2)
            
    def setup_plot(self):
        """Configure plot appearance."""
        if self.scenario == 'acceleration':
            # Motion plot
            self.ax_motion.set_xlim(0, 10)
            self.ax_motion.set_ylim(0, 2)
            self.ax_motion.set_xlabel('Position')
            self.ax_motion.set_ylabel('Velocity (c)')
            self.ax_motion.set_title('Relativistic Acceleration')
            self.ax_motion.grid(True, alpha=0.3)
            
            # Gamma factor plot
            self.ax_gamma.set_xlim(0, 10)
            self.ax_gamma.set_ylim(1, 10)
            self.ax_gamma.set_xlabel('Time')
            self.ax_gamma.set_ylabel('γ factor')
            self.ax_gamma.set_title('Lorentz Factor vs Time')
            self.ax_gamma.grid(True, alpha=0.3)
            
            # Plot elements
            self.trajectory_line, = self.ax_motion.plot([], [], 'b-', linewidth=2, label='Trajectory')
            self.particle_dot, = self.ax_motion.plot([], [], 'ro', markersize=8)
            self.gamma_line, = self.ax_gamma.plot([], [], 'r-', linewidth=2, label='γ(t)')
            
            self.ax_motion.legend()
            self.ax_gamma.legend()
            
        elif self.scenario == 'twin_paradox':
            self.ax_motion.set_xlim(0, 15)
            self.ax_motion.set_ylim(0, 10)
            self.ax_motion.set_xlabel('Time (years)')
            self.ax_motion.set_ylabel('Age (years)')
            self.ax_motion.set_title('Twin Paradox')
            self.ax_motion.grid(True, alpha=0.3)
            
            # Plot elements
            self.earth_twin_line, = self.ax_motion.plot([], [], 'b-', linewidth=3, label='Earth twin')
            self.space_twin_line, = self.ax_motion.plot([], [], 'r-', linewidth=3, label='Space twin')
            
            self.ax_motion.legend()
            
    def relativistic_acceleration_step(self, v: float, a_proper: float, dt: float) -> float:
        """One step of relativistic acceleration."""
        gamma = 1 / np.sqrt(1 - v**2)
        # Relativistic equation of motion: dp/dt = F, where p = γmv
        # For constant proper acceleration: dv/dt = a(1-v²)^(3/2)
        dv_dt = a_proper * (1 - v**2)**(3/2)
        return v + dv_dt * dt
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        if self.scenario == 'acceleration':
            self.times = [0]
            self.positions = [self.initial_position]
            self.velocities = [self.initial_velocity]
            self.gammas = [1.0]
            return [self.trajectory_line, self.particle_dot, self.gamma_line]
        elif self.scenario == 'twin_paradox':
            return [self.earth_twin_line, self.space_twin_line]
            
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        if self.scenario == 'acceleration':
            return self.animate_acceleration(frame)
        elif self.scenario == 'twin_paradox':
            return self.animate_twin_paradox(frame)
            
    def animate_acceleration(self, frame: int) -> List:
        """Animate relativistic acceleration."""
        if frame == 0:
            return [self.trajectory_line, self.particle_dot, self.gamma_line]
            
        # Update motion
        current_v = self.velocities[-1]
        new_v = self.relativistic_acceleration_step(current_v, self.proper_acceleration, self.dt)
        
        # Ensure v < c
        new_v = min(new_v, 0.99)
        
        # Update position
        new_x = self.positions[-1] + new_v * self.dt
        new_t = self.times[-1] + self.dt
        
        # Calculate gamma factor
        gamma = 1 / np.sqrt(1 - new_v**2)
        
        # Store values
        self.times.append(new_t)
        self.positions.append(new_x)
        self.velocities.append(new_v)
        self.gammas.append(gamma)
        
        # Limit data length
        if len(self.times) > 1000:
            self.times.pop(0)
            self.positions.pop(0)
            self.velocities.pop(0)
            self.gammas.pop(0)
            
        # Update plots
        self.trajectory_line.set_data(self.positions, self.velocities)
        if len(self.positions) > 0:
            self.particle_dot.set_data([self.positions[-1]], [self.velocities[-1]])
            
        self.gamma_line.set_data(self.times, self.gammas)
        
        return [self.trajectory_line, self.particle_dot, self.gamma_line]
        
    def animate_twin_paradox(self, frame: int) -> List:
        """Animate the twin paradox."""
        total_time = 12.0
        t = frame * 0.1
        
        if t > total_time:
            t = total_time
            
        # Earth twin ages normally
        earth_times = np.linspace(0, t, 100)
        earth_ages = earth_times + 20  # Start at age 20
        
        # Space twin trajectory
        space_times = []
        space_ages = []
        
        current_age = 20  # Starting age
        
        if t <= self.travel_time:
            # Outbound journey
            proper_time_elapsed = t / self.gamma_travel
            space_times = np.linspace(0, t, 100)
            space_ages = np.linspace(20, 20 + proper_time_elapsed, 100)
        elif t <= 2 * self.travel_time:
            # Return journey
            outbound_proper_time = self.travel_time / self.gamma_travel
            return_time = t - self.travel_time
            return_proper_time = return_time / self.gamma_travel
            
            space_times = np.linspace(0, t, 100)
            total_proper_time = outbound_proper_time + return_proper_time
            space_ages = np.linspace(20, 20 + total_proper_time, 100)
        else:
            # After return, ages normally again
            total_proper_travel_time = 2 * self.travel_time / self.gamma_travel
            post_return_time = t - 2 * self.travel_time
            
            space_times = np.linspace(0, t, 100)
            final_age = 20 + total_proper_travel_time + post_return_time
            space_ages = np.linspace(20, final_age, 100)
            
        # Update plots
        self.earth_twin_line.set_data(earth_times, earth_ages)
        if len(space_times) > 0:
            self.space_twin_line.set_data(space_times, space_ages)
            
        return [self.earth_twin_line, self.space_twin_line]


class GravitationalLensing:
    """Visualize gravitational lensing effects."""
    
    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(1, 2, figsize=figsize)
        
    def plot_light_bending(self, ax, mass: float = 1e30):
        """Plot light ray bending around a massive object."""
        # Schwarzschild radius (in arbitrary units)
        G = 6.67e-11
        c = 3e8
        rs = 2 * G * mass / c**2 / 1e9  # Convert to more reasonable units
        
        # Massive object at center
        ax.add_patch(Circle((0, 0), rs, color='black', label='Massive object'))
        
        # Straight light path (no gravity)
        x_straight = np.linspace(-5, 5, 100)
        y_straight = np.ones_like(x_straight) * 2
        ax.plot(x_straight, y_straight, 'b--', linewidth=2, alpha=0.7, label='Path without gravity')
        
        # Bent light path (approximate)
        x_bent = np.linspace(-5, 5, 200)
        y_bent = np.zeros_like(x_bent)
        
        for i, x in enumerate(x_bent):
            r = np.sqrt(x**2 + 2**2)  # Distance from center
            if r > rs:
                # Simple approximation for light bending
                deflection_angle = 4 * rs / r  # Simplified formula
                if abs(x) < 3:  # Only bend near the mass
                    y_bent[i] = 2 - deflection_angle * np.exp(-abs(x)/2)
                else:
                    y_bent[i] = 2
            else:
                y_bent[i] = 2
                
        ax.plot(x_bent, y_bent, 'r-', linewidth=2, label='Bent light path')
        
        # Add light rays
        for y_start in [1.5, 2.5]:
            y_bent_ray = np.zeros_like(x_bent)
            for i, x in enumerate(x_bent):
                r = np.sqrt(x**2 + y_start**2)
                if r > rs and abs(x) < 3:
                    deflection_angle = 4 * rs / r
                    y_bent_ray[i] = y_start - deflection_angle * np.exp(-abs(x)/2)
                else:
                    y_bent_ray[i] = y_start
            ax.plot(x_bent, y_bent_ray, 'orange', linewidth=1, alpha=0.8)
            
        ax.set_xlim(-6, 6)
        ax.set_ylim(-1, 4)
        ax.set_aspect('equal')
        ax.set_xlabel('Distance')
        ax.set_ylabel('Distance')
        ax.set_title('Gravitational Light Bending')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_einstein_ring(self, ax):
        """Plot Einstein ring formation."""
        # Source, lens, and observer positions
        ax.scatter(0, 0, s=200, c='yellow', marker='*', label='Source', zorder=5)
        ax.scatter(0, 3, s=150, c='red', marker='o', label='Lens', zorder=5)
        ax.scatter(0, 6, s=100, c='blue', marker='s', label='Observer', zorder=5)
        
        # Einstein ring
        einstein_radius = 1.5
        circle = Circle((0, 3), einstein_radius, fill=False, color='orange', 
                       linewidth=3, linestyle='--', label='Einstein Ring')
        ax.add_patch(circle)
        
        # Light paths showing lensing
        angles = np.linspace(0, 2*np.pi, 12)
        for angle in angles:
            # From source to lens
            x1 = einstein_radius * np.cos(angle)
            y1 = 3 + einstein_radius * np.sin(angle)
            ax.plot([0, x1], [0, y1], 'orange', linewidth=2, alpha=0.7)
            
            # From lens to observer
            ax.plot([x1, 0], [y1, 6], 'orange', linewidth=2, alpha=0.7)
            
        # Direct line (blocked by lens)
        ax.plot([0, 0], [0, 6], 'k--', linewidth=2, alpha=0.3, label='Direct path (blocked)')
        
        ax.set_xlim(-3, 3)
        ax.set_ylim(-1, 7)
        ax.set_aspect('equal')
        ax.set_xlabel('Distance')
        ax.set_ylabel('Distance')
        ax.set_title('Einstein Ring Formation')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def show(self):
        """Display gravitational lensing visualizations."""
        self.plot_light_bending(self.axes[0])
        self.plot_einstein_ring(self.axes[1])
        
        plt.tight_layout()
        plt.show()


class BlackHoleVisualization:
    """Visualize black hole properties and effects."""
    
    def __init__(self, figsize=(15, 5)):
        self.fig, self.axes = plt.subplots(1, 3, figsize=figsize)
        
    def plot_schwarzschild_geometry(self, ax, mass: float = 1.0):
        """Plot Schwarzschild spacetime geometry."""
        # Radial coordinates
        r = np.linspace(0.1, 10, 200)
        rs = 2.0  # Schwarzschild radius in arbitrary units
        
        # Metric components (simplified visualization)
        g_tt = -(1 - rs/r)  # Time component
        g_rr = 1/(1 - rs/r)  # Radial component
        
        # Plot metric components
        ax.plot(r, g_tt, 'b-', linewidth=2, label='g_tt (time)')
        ax.plot(r, 1/g_rr, 'r-', linewidth=2, label='1/g_rr (space)')
        
        # Event horizon
        ax.axvline(rs, color='black', linewidth=3, linestyle='--', 
                  label=f'Event Horizon (r_s = {rs})')
        
        # Photon sphere
        ax.axvline(1.5*rs, color='orange', linewidth=2, linestyle=':', 
                  label='Photon Sphere (1.5 r_s)')
        
        ax.set_xlim(0, 8)
        ax.set_ylim(-5, 5)
        ax.set_xlabel('Radial Distance (r/r_s)')
        ax.set_ylabel('Metric Component')
        ax.set_title('Schwarzschild Metric Components')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add singularity warning
        ax.text(0.5, -4, 'Singularity\nr = 0', ha='center', va='center',
               bbox=dict(boxstyle="round,pad=0.3", facecolor="red", alpha=0.7))
        
    def plot_tidal_forces(self, ax):
        """Plot tidal force effects near a black hole."""
        # Object approaching black hole
        bh_pos = np.array([0, 0])
        rs = 1.0
        
        # Draw black hole
        ax.add_patch(Circle(bh_pos, rs, color='black'))
        ax.add_patch(Circle(bh_pos, rs*0.8, color='darkgray', alpha=0.5))
        
        # Object at different distances
        distances = [3, 4, 6]
        colors = ['red', 'orange', 'yellow']
        
        for i, (dist, color) in enumerate(zip(distances, colors)):
            # Object position
            obj_pos = np.array([dist, 0])
            
            # Draw object (gets stretched by tidal forces)
            if dist <= 4:  # Strong tidal forces
                # Spaghettification
                ellipse = Ellipse(obj_pos, 0.3, 0.8 + (4-dist)*0.5, 
                                 angle=0, facecolor=color, alpha=0.7)
            else:  # Weak tidal forces
                ellipse = Circle(obj_pos, 0.2, facecolor=color, alpha=0.7)
                
            ax.add_patch(ellipse)
            
            # Tidal force arrows
            if dist <= 5:
                # Radial stretching
                ax.arrow(obj_pos[0], obj_pos[1]+0.3, 0, 0.2, 
                        head_width=0.1, head_length=0.05, fc=color, ec=color)
                ax.arrow(obj_pos[0], obj_pos[1]-0.3, 0, -0.2, 
                        head_width=0.1, head_length=0.05, fc=color, ec=color)
                
                # Tangential compression
                ax.arrow(obj_pos[0]+0.2, obj_pos[1], -0.1, 0, 
                        head_width=0.05, head_length=0.03, fc=color, ec=color)
                ax.arrow(obj_pos[0]-0.2, obj_pos[1], 0.1, 0, 
                        head_width=0.05, head_length=0.03, fc=color, ec=color)
                        
        ax.set_xlim(-2, 8)
        ax.set_ylim(-3, 3)
        ax.set_aspect('equal')
        ax.set_xlabel('Distance from Black Hole')
        ax.set_ylabel('Distance')
        ax.set_title('Tidal Forces (Spaghettification)')
        
        # Add labels
        ax.text(3, -2, 'Strong\nTidal Forces', ha='center', color='red', fontweight='bold')
        ax.text(6, -2, 'Weak\nTidal Forces', ha='center', color='orange', fontweight='bold')
        
    def plot_accretion_disk(self, ax):
        """Plot black hole with accretion disk."""
        # Black hole
        bh_radius = 0.5
        ax.add_patch(Circle((0, 0), bh_radius, color='black', zorder=5))
        
        # Accretion disk (multiple rings with temperature colors)
        disk_radii = np.linspace(1, 4, 20)
        temperatures = 1000 / disk_radii**0.75  # Temperature profile
        
        for i, (r, temp) in enumerate(zip(disk_radii, temperatures)):
            # Color based on temperature (blue = hot, red = cool)
            color_intensity = (temp - min(temperatures)) / (max(temperatures) - min(temperatures))
            color = plt.cm.hot(1 - color_intensity)
            
            # Draw disk ring
            ring = Circle((0, 0), r, fill=False, linewidth=8, 
                         color=color, alpha=0.7)
            ax.add_patch(ring)
            
        # Jets
        jet_length = 6
        jet_width = 0.3
        
        # Upward jet
        ax.add_patch(Rectangle((-jet_width/2, bh_radius), jet_width, jet_length, 
                              facecolor='cyan', alpha=0.8))
        # Downward jet
        ax.add_patch(Rectangle((-jet_width/2, -bh_radius-jet_length), jet_width, jet_length, 
                              facecolor='cyan', alpha=0.8))
        
        # Add spiral structure
        theta = np.linspace(0, 6*np.pi, 500)
        r_spiral = 1.5 + 0.5 * theta / (2*np.pi)
        x_spiral = r_spiral * np.cos(theta)
        y_spiral = r_spiral * np.sin(theta)
        
        # Only plot where r < 4
        mask = r_spiral < 4
        ax.plot(x_spiral[mask], y_spiral[mask], 'white', linewidth=1, alpha=0.6)
        
        ax.set_xlim(-5, 5)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')
        ax.set_xlabel('Distance')
        ax.set_ylabel('Distance')
        ax.set_title('Black Hole with Accretion Disk')
        
        # Temperature colorbar (approximation)
        sm = plt.cm.ScalarMappable(cmap='hot', norm=plt.Normalize(vmin=0, vmax=1))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Temperature (relative)', rotation=270, labelpad=15)
        
    def show(self):
        """Display black hole visualizations."""
        self.plot_schwarzschild_geometry(self.axes[0])
        self.plot_tidal_forces(self.axes[1])
        self.plot_accretion_disk(self.axes[2])
        
        plt.tight_layout()
        plt.show()


def create_relativistic_velocity_demo():
    """Interactive demo of relativistic velocity addition."""
    plot = InteractivePhysicsPlot(figsize=(12, 8))
    
    # Parameters
    params = {
        'v1': 0.5,  # First velocity (in units of c)
        'v2': 0.3   # Second velocity (in units of c)
    }
    
    def update_velocity_addition(val=None):
        """Update relativistic velocity addition demonstration."""
        plot.main_ax.clear()
        
        v1 = params['v1']
        v2 = params['v2']
        
        # Classical addition
        v_classical = v1 + v2
        
        # Relativistic addition: v = (v1 + v2)/(1 + v1*v2/c²)
        v_relativistic = (v1 + v2) / (1 + v1 * v2)
        
        # Create velocity diagram
        velocities = np.linspace(0, 1, 100)
        classical_sums = velocities + v2
        relativistic_sums = (velocities + v2) / (1 + velocities * v2)
        
        plot.main_ax.plot(velocities, classical_sums, 'b--', linewidth=2, 
                         label='Classical: v₁ + v₂')
        plot.main_ax.plot(velocities, relativistic_sums, 'r-', linewidth=3, 
                         label='Relativistic: (v₁ + v₂)/(1 + v₁v₂/c²)')
        
        # Highlight current values
        plot.main_ax.scatter([v1], [v_classical], s=100, c='blue', zorder=5, 
                           label=f'Classical result: {v_classical:.2f}c')
        plot.main_ax.scatter([v1], [v_relativistic], s=100, c='red', zorder=5,
                           label=f'Relativistic result: {v_relativistic:.2f}c')
        
        # Speed of light limit
        plot.main_ax.axhline(1, color='black', linestyle='-', alpha=0.5, 
                           label='Speed of light (c)')
        
        plot.main_ax.set_xlim(0, 1)
        plot.main_ax.set_ylim(0, 2)
        plot.main_ax.set_xlabel('First velocity v₁ (c)')
        plot.main_ax.set_ylabel('Combined velocity (c)')
        plot.main_ax.set_title('Relativistic Velocity Addition')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add controls
    plot.add_slider('v₁ (c)', 0.1, 0.9, params['v1'], 
                   lambda val: (params.update({'v1': val}), update_velocity_addition()))
    plot.add_slider('v₂ (c)', 0.1, 0.9, params['v2'],
                   lambda val: (params.update({'v2': val}), update_velocity_addition()))
    
    # Initial plot
    update_velocity_addition()
    
    return plot


# Convenience functions for quick demonstrations
def demo_spacetime_diagrams():
    """Quick spacetime diagram demo."""
    diagrams = SpacetimeDiagram()
    diagrams.show()

def demo_relativistic_motion():
    """Quick relativistic motion demo."""
    sim = RelativisticMotion(scenario='acceleration')
    sim.start_animation(interval=50, frames=1000)
    sim.show()

def demo_twin_paradox():
    """Quick twin paradox demo."""
    sim = RelativisticMotion(scenario='twin_paradox')
    sim.start_animation(interval=100, frames=120)
    sim.show()

def demo_gravitational_lensing():
    """Quick gravitational lensing demo."""
    lensing = GravitationalLensing()
    lensing.show()

def demo_black_holes():
    """Quick black hole visualization demo."""
    bh_viz = BlackHoleVisualization()
    bh_viz.show()

def demo_velocity_addition():
    """Quick relativistic velocity addition demo."""
    demo = create_relativistic_velocity_demo()
    demo.show()