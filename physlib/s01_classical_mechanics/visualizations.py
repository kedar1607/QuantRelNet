"""Visual simulations for classical mechanics concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import List, Tuple, Optional
from ..visualization import PhysicsAnimation, ParticleTracker, setup_physics_plot, InteractivePhysicsPlot
from . import newton, energy, momentum, gravity


class ProjectileMotion(PhysicsAnimation):
    """Animate projectile motion with air resistance option."""
    
    def __init__(self, v0: float, angle: float, drag_coeff: float = 0.0, figsize=(12, 6)):
        super().__init__(figsize)
        self.v0 = v0
        self.angle = np.radians(angle)
        self.drag_coeff = drag_coeff
        self.g = 9.81
        self.dt = 0.02
        
        # Initial conditions
        self.x0, self.y0 = 0, 0
        self.vx0 = v0 * np.cos(self.angle)
        self.vy0 = v0 * np.sin(self.angle)
        
        # Trajectory storage
        self.x_data = []
        self.y_data = []
        
        # Plot elements
        self.trajectory_line, = self.ax.plot([], [], 'b-', alpha=0.7, label='Trajectory')
        self.projectile = Circle((0, 0), 0.5, color='red', animated=True)
        self.ax.add_patch(self.projectile)
        
        # Velocity vector
        self.velocity_arrow = self.ax.annotate('', xy=(0, 0), xytext=(0, 0),
                                              arrowprops=dict(arrowstyle='->', color='green', lw=2))
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        max_range = (self.v0**2 * np.sin(2*self.angle)) / self.g
        max_height = (self.v0**2 * np.sin(self.angle)**2) / (2*self.g)
        
        self.ax.set_xlim(0, max_range * 1.1)
        self.ax.set_ylim(0, max_height * 1.2)
        self.ax.set_xlabel('Distance (m)')
        self.ax.set_ylabel('Height (m)')
        self.ax.set_title(f'Projectile Motion (v₀={self.v0} m/s, θ={np.degrees(self.angle):.1f}°)')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.x_data = [self.x0]
        self.y_data = [self.y0]
        self.trajectory_line.set_data([], [])
        self.projectile.center = (self.x0, self.y0)
        return [self.trajectory_line, self.projectile, self.velocity_arrow]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * self.dt
        
        if self.drag_coeff == 0:
            # No air resistance
            x = self.x0 + self.vx0 * t
            y = self.y0 + self.vy0 * t - 0.5 * self.g * t**2
            vx = self.vx0
            vy = self.vy0 - self.g * t
        else:
            # With air resistance (simplified)
            exp_term = np.exp(-self.drag_coeff * t)
            x = (self.vx0 / self.drag_coeff) * (1 - exp_term)
            y = ((self.vy0 + self.g/self.drag_coeff) / self.drag_coeff) * (1 - exp_term) - (self.g * t) / self.drag_coeff
            vx = self.vx0 * exp_term
            vy = (self.vy0 + self.g/self.drag_coeff) * exp_term - self.g/self.drag_coeff
            
        if y < 0:  # Hit ground
            return [self.trajectory_line, self.projectile, self.velocity_arrow]
            
        self.x_data.append(x)
        self.y_data.append(y)
        
        # Update trajectory
        self.trajectory_line.set_data(self.x_data, self.y_data)
        
        # Update projectile position
        self.projectile.center = (x, y)
        
        # Update velocity vector
        scale = 2.0
        self.velocity_arrow.xy = (x + vx * scale, y + vy * scale)
        self.velocity_arrow.xytext = (x, y)
        
        return [self.trajectory_line, self.projectile, self.velocity_arrow]


class PendulumSimulation(PhysicsAnimation):
    """Animate a simple pendulum with customizable parameters."""
    
    def __init__(self, length: float = 1.0, theta0: float = 30.0, damping: float = 0.0, figsize=(8, 8)):
        super().__init__(figsize)
        self.L = length
        self.theta0 = np.radians(theta0)
        self.damping = damping
        self.g = 9.81
        self.dt = 0.02
        
        # Initial conditions
        self.theta = self.theta0
        self.omega = 0.0  # Angular velocity
        
        # Plot elements
        self.pendulum_line, = self.ax.plot([], [], 'ko-', lw=2, markersize=10)
        self.trail_line, = self.ax.plot([], [], 'b-', alpha=0.3, lw=1)
        
        self.trail_x = []
        self.trail_y = []
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        margin = self.L * 1.2
        self.ax.set_xlim(-margin, margin)
        self.ax.set_ylim(-margin, margin/2)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        self.ax.set_title(f'Simple Pendulum (L={self.L}m, θ₀={np.degrees(self.theta0):.1f}°)')
        self.ax.grid(True, alpha=0.3)
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.theta = self.theta0
        self.omega = 0.0
        self.trail_x = []
        self.trail_y = []
        return [self.pendulum_line, self.trail_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Small angle approximation: d²θ/dt² = -(g/L)sin(θ) - γ*dθ/dt
        alpha = -(self.g / self.L) * np.sin(self.theta) - self.damping * self.omega
        
        # Update angular velocity and position
        self.omega += alpha * self.dt
        self.theta += self.omega * self.dt
        
        # Convert to Cartesian coordinates
        x = self.L * np.sin(self.theta)
        y = -self.L * np.cos(self.theta)
        
        # Update pendulum
        self.pendulum_line.set_data([0, x], [0, y])
        
        # Update trail
        self.trail_x.append(x)
        self.trail_y.append(y)
        if len(self.trail_x) > 200:  # Limit trail length
            self.trail_x.pop(0)
            self.trail_y.pop(0)
            
        self.trail_line.set_data(self.trail_x, self.trail_y)
        
        return [self.pendulum_line, self.trail_line]


class SpringMassSystem(PhysicsAnimation):
    """Animate a spring-mass system with damping."""
    
    def __init__(self, mass: float = 1.0, k: float = 10.0, damping: float = 0.1, 
                 x0: float = 1.0, figsize=(10, 6)):
        super().__init__(figsize)
        self.m = mass
        self.k = k
        self.c = damping
        self.x0 = x0
        self.dt = 0.01
        
        # Initial conditions
        self.x = x0
        self.v = 0.0
        
        # Natural frequency and damping ratio
        self.omega_n = np.sqrt(k / mass)
        self.zeta = damping / (2 * np.sqrt(k * mass))
        
        # Plot elements
        self.mass_patch = Circle((0, 0), 0.1, color='red', animated=True)
        self.ax.add_patch(self.mass_patch)
        
        self.spring_line, = self.ax.plot([], [], 'b-', lw=3)
        self.position_line, = self.ax.plot([], [], 'r-', alpha=0.7)
        
        self.time_data = []
        self.position_data = []
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Create subplots: spring animation and position vs time
        self.fig.clear()
        self.ax_spring = self.fig.add_subplot(211)
        self.ax_plot = self.fig.add_subplot(212)
        
        # Spring animation subplot
        self.ax_spring.set_xlim(-2, 2)
        self.ax_spring.set_ylim(-0.5, 0.5)
        self.ax_spring.set_aspect('equal')
        self.ax_spring.set_title(f'Spring-Mass System (m={self.m}kg, k={self.k}N/m)')
        self.ax_spring.axhline(0, color='k', linewidth=0.5)
        
        # Position plot subplot
        self.ax_plot.set_xlim(0, 10)
        self.ax_plot.set_ylim(-self.x0*1.5, self.x0*1.5)
        self.ax_plot.set_xlabel('Time (s)')
        self.ax_plot.set_ylabel('Position (m)')
        self.ax_plot.grid(True, alpha=0.3)
        
        # Add elements to spring subplot
        self.mass_patch = Circle((0, 0), 0.05, color='red', animated=True)
        self.ax_spring.add_patch(self.mass_patch)
        self.spring_line, = self.ax_spring.plot([], [], 'b-', lw=3)
        
        # Add elements to position subplot
        self.position_line, = self.ax_plot.plot([], [], 'r-', lw=2, label='Position')
        self.ax_plot.legend()
        
    def draw_spring(self, x_pos: float, n_coils: int = 10):
        """Draw a spring from origin to mass position."""
        if abs(x_pos) < 0.01:
            x_pos = 0.01  # Avoid division by zero
            
        # Create spring coil coordinates
        t = np.linspace(0, n_coils * 2 * np.pi, 200)
        spring_x = np.linspace(-1, x_pos - 0.05, len(t))
        spring_y = 0.1 * np.sin(t) * (1 - np.abs(spring_x) / max(abs(x_pos), 0.1))
        
        return spring_x, spring_y
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.x = self.x0
        self.v = 0.0
        self.time_data = []
        self.position_data = []
        return [self.mass_patch, self.spring_line, self.position_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * self.dt
        
        # Force calculation: F = -kx - cv
        force = -self.k * self.x - self.c * self.v
        acceleration = force / self.m
        
        # Update position and velocity
        self.v += acceleration * self.dt
        self.x += self.v * self.dt
        
        # Update mass position
        self.mass_patch.center = (self.x, 0)
        
        # Update spring
        spring_x, spring_y = self.draw_spring(self.x)
        self.spring_line.set_data(spring_x, spring_y)
        
        # Update position plot
        self.time_data.append(t)
        self.position_data.append(self.x)
        
        if len(self.time_data) > 500:  # Limit data length
            self.time_data.pop(0)
            self.position_data.pop(0)
            
        self.position_line.set_data(self.time_data, self.position_data)
        
        # Update plot limits if needed
        if t > 10:
            self.ax_plot.set_xlim(t-10, t)
            
        return [self.mass_patch, self.spring_line, self.position_line]


class CollisionSimulation(PhysicsAnimation):
    """Simulate elastic and inelastic collisions between particles."""
    
    def __init__(self, m1: float = 1.0, m2: float = 2.0, v1: float = 5.0, v2: float = -2.0,
                 restitution: float = 1.0, figsize=(12, 6)):
        super().__init__(figsize)
        self.m1, self.m2 = m1, m2
        self.v1_initial, self.v2_initial = v1, v2
        self.e = restitution  # Coefficient of restitution
        self.dt = 0.02
        
        # Particle properties
        self.x1, self.x2 = -5.0, 5.0
        self.v1, self.v2 = v1, v2
        self.r1, self.r2 = 0.3, 0.4  # Radii proportional to mass
        
        self.collision_occurred = False
        self.collision_time = None
        
        # Plot elements
        self.particle1 = Circle((self.x1, 0), self.r1, color='blue', animated=True)
        self.particle2 = Circle((self.x2, 0), self.r2, color='red', animated=True)
        self.ax.add_patch(self.particle1)
        self.ax.add_patch(self.particle2)
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-2, 2)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('Position (m)')
        self.ax.set_title(f'Particle Collision (m₁={self.m1}kg, m₂={self.m2}kg, e={self.e})')
        
        # Add center line
        self.ax.axhline(0, color='k', linewidth=0.5, alpha=0.3)
        
        # Add text for velocities
        self.velocity_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes, 
                                         verticalalignment='top', fontsize=10)
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        self.x1, self.x2 = -5.0, 5.0
        self.v1, self.v2 = self.v1_initial, self.v2_initial
        self.collision_occurred = False
        self.collision_time = None
        
        self.particle1.center = (self.x1, 0)
        self.particle2.center = (self.x2, 0)
        
        return [self.particle1, self.particle2]
        
    def check_collision(self) -> bool:
        """Check if particles are colliding."""
        distance = abs(self.x2 - self.x1)
        return distance <= (self.r1 + self.r2)
        
    def handle_collision(self):
        """Handle collision using conservation laws."""
        if self.collision_occurred:
            return
            
        # Conservation of momentum and energy with restitution
        v1_new = ((self.m1 - self.e * self.m2) * self.v1 + (1 + self.e) * self.m2 * self.v2) / (self.m1 + self.m2)
        v2_new = ((self.m2 - self.e * self.m1) * self.v2 + (1 + self.e) * self.m1 * self.v1) / (self.m1 + self.m2)
        
        self.v1 = v1_new
        self.v2 = v2_new
        self.collision_occurred = True
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        # Update positions
        self.x1 += self.v1 * self.dt
        self.x2 += self.v2 * self.dt
        
        # Check for collision
        if self.check_collision() and not self.collision_occurred:
            self.handle_collision()
            
        # Update particle positions
        self.particle1.center = (self.x1, 0)
        self.particle2.center = (self.x2, 0)
        
        # Update velocity display
        momentum_before = self.m1 * self.v1_initial + self.m2 * self.v2_initial
        momentum_current = self.m1 * self.v1 + self.m2 * self.v2
        
        self.velocity_text.set_text(
            f'v₁ = {self.v1:.2f} m/s\n'
            f'v₂ = {self.v2:.2f} m/s\n'
            f'Total momentum: {momentum_current:.2f} kg⋅m/s\n'
            f'Initial momentum: {momentum_before:.2f} kg⋅m/s'
        )
        
        return [self.particle1, self.particle2]


def create_orbital_motion_demo():
    """Create an interactive demo of orbital mechanics."""
    plot = InteractivePhysicsPlot(figsize=(12, 10))
    
    # Initial parameters
    params = {
        'mass_central': 1e20,
        'mass_orbiting': 1e10,
        'initial_distance': 10.0,
        'initial_velocity': 15.0
    }
    
    # Create particle tracker
    tracker = ParticleTracker(max_particles=1, trail_length=200)
    
    def update_orbit(val=None):
        """Update orbital simulation with new parameters."""
        plot.main_ax.clear()
        
        # Central mass (fixed at origin)
        plot.main_ax.scatter(0, 0, s=200, c='yellow', marker='o', label='Central Mass')
        
        # Set up gravitational force function
        def gravitational_force(pos, vel, mass):
            r = np.linalg.norm(pos)
            if r < 0.1:  # Avoid singularity
                return np.array([0.0, 0.0])
            
            force_magnitude = gravity.gravitational_constant() * params['mass_central'] * mass / r**2
            force_direction = -pos / r  # Toward center
            return force_magnitude * force_direction
        
        # Reset particle
        tracker.particles.clear()
        tracker.add_particle(
            position=np.array([params['initial_distance'], 0.0]),
            velocity=np.array([0.0, params['initial_velocity']]),
            mass=params['mass_orbiting'],
            color='blue',
            size=50
        )
        
        # Simulate orbit
        for _ in range(500):
            tracker.update_particles(0.1, gravitational_force)
            
        # Plot result
        tracker.plot_particles(plot.main_ax)
        
        plot.main_ax.set_xlim(-20, 20)
        plot.main_ax.set_ylim(-20, 20)
        plot.main_ax.set_aspect('equal')
        plot.main_ax.set_title('Orbital Motion Simulation')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add sliders
    plot.add_slider('Distance', 5.0, 20.0, params['initial_distance'], 
                   lambda val: (params.update({'initial_distance': val}), update_orbit()))
    plot.add_slider('Velocity', 5.0, 25.0, params['initial_velocity'],
                   lambda val: (params.update({'initial_velocity': val}), update_orbit()))
    
    # Initial plot
    update_orbit()
    
    return plot


# Convenience functions for quick demonstrations
def demo_projectile():
    """Quick projectile motion demo."""
    sim = ProjectileMotion(v0=20, angle=45, drag_coeff=0.05)
    sim.start_animation(interval=30, frames=300)
    sim.show()

def demo_pendulum():
    """Quick pendulum demo."""
    sim = PendulumSimulation(length=2.0, theta0=45, damping=0.02)
    sim.start_animation(interval=30, frames=500)
    sim.show()

def demo_spring_mass():
    """Quick spring-mass system demo."""
    sim = SpringMassSystem(mass=2.0, k=20.0, damping=0.3, x0=1.5)
    sim.start_animation(interval=20, frames=800)
    sim.show()

def demo_collision():
    """Quick collision demo."""
    sim = CollisionSimulation(m1=1.0, m2=3.0, v1=8.0, v2=-2.0, restitution=0.8)
    sim.start_animation(interval=40, frames=400)
    sim.show()