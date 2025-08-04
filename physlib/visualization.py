"""Core visualization framework for physics simulations.

This module provides a unified interface for creating animations and
interactive visualizations of physics concepts using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
from typing import Callable, Optional, List, Tuple, Dict, Any
from abc import ABC, abstractmethod


class PhysicsAnimation(ABC):
    """Base class for physics animations."""
    
    def __init__(self, figsize: Tuple[float, float] = (10, 8)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.animation = None
        self.is_running = False
        
    @abstractmethod
    def init_plot(self) -> List:
        """Initialize the plot elements. Return list of artists to animate."""
        pass
        
    @abstractmethod
    def animate(self, frame: int) -> List:
        """Update plot for given frame. Return list of artists."""
        pass
        
    def start_animation(self, interval: int = 50, frames: int = 200):
        """Start the animation."""
        self.animation = animation.FuncAnimation(
            self.fig, self.animate, init_func=self.init_plot,
            frames=frames, interval=interval, blit=True, repeat=True
        )
        self.is_running = True
        
    def stop_animation(self):
        """Stop the animation."""
        if self.animation:
            self.animation.event_source.stop()
            self.is_running = False
            
    def show(self):
        """Display the plot."""
        plt.show()


class InteractivePhysicsPlot:
    """Interactive plot with sliders for parameter control."""
    
    def __init__(self, figsize: Tuple[float, float] = (12, 8)):
        self.fig = plt.figure(figsize=figsize)
        self.main_ax = plt.subplot2grid((4, 4), (0, 0), colspan=4, rowspan=3)
        self.sliders = {}
        self.buttons = {}
        self.slider_row = 0
        
    def add_slider(self, name: str, min_val: float, max_val: float, 
                   initial: float, callback: Callable[[float], None]):
        """Add a parameter slider."""
        ax_slider = plt.subplot2grid((4, 4), (3, self.slider_row), colspan=1)
        slider = Slider(ax_slider, name, min_val, max_val, valinit=initial)
        slider.on_changed(callback)
        self.sliders[name] = slider
        self.slider_row += 1
        
    def add_button(self, name: str, callback: Callable[[], None], position: Tuple[int, int]):
        """Add a control button."""
        ax_button = plt.subplot2grid((4, 4), position, colspan=1)
        button = Button(ax_button, name)
        button.on_clicked(lambda x: callback())
        self.buttons[name] = button
        
    def show(self):
        """Display the interactive plot."""
        plt.tight_layout()
        plt.show()


class VectorField:
    """Utility for plotting vector fields."""
    
    @staticmethod
    def plot_2d_field(ax, x_range: Tuple[float, float], y_range: Tuple[float, float],
                     field_func: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]],
                     density: int = 20, scale: float = 1.0, color: str = 'blue'):
        """Plot a 2D vector field."""
        x = np.linspace(x_range[0], x_range[1], density)
        y = np.linspace(y_range[0], y_range[1], density)
        X, Y = np.meshgrid(x, y)
        
        U, V = field_func(X, Y)
        ax.quiver(X, Y, U, V, scale=scale, color=color, alpha=0.7)
        
    @staticmethod
    def plot_streamlines(ax, x_range: Tuple[float, float], y_range: Tuple[float, float],
                        field_func: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]],
                        density: int = 50, color: str = 'red'):
        """Plot streamlines of a 2D vector field."""
        x = np.linspace(x_range[0], x_range[1], density)
        y = np.linspace(y_range[0], y_range[1], density)
        X, Y = np.meshgrid(x, y)
        
        U, V = field_func(X, Y)
        ax.streamplot(X, Y, U, V, color=color, density=1.5, linewidth=1, alpha=0.8)


class ParticleTracker:
    """Track and visualize particle trajectories."""
    
    def __init__(self, max_particles: int = 100, trail_length: int = 50):
        self.max_particles = max_particles
        self.trail_length = trail_length
        self.particles = []
        self.trails = []
        
    def add_particle(self, position: np.ndarray, velocity: np.ndarray, 
                    mass: float = 1.0, color: str = 'blue', size: float = 10):
        """Add a particle to track."""
        particle = {
            'position': np.array(position),
            'velocity': np.array(velocity),
            'mass': mass,
            'color': color,
            'size': size,
            'trail': [np.array(position)]
        }
        self.particles.append(particle)
        
    def update_particles(self, dt: float, force_func: Optional[Callable] = None):
        """Update particle positions using basic physics."""
        for particle in self.particles:
            if force_func:
                force = force_func(particle['position'], particle['velocity'], particle['mass'])
                acceleration = force / particle['mass']
                particle['velocity'] += acceleration * dt
                
            particle['position'] += particle['velocity'] * dt
            particle['trail'].append(particle['position'].copy())
            
            if len(particle['trail']) > self.trail_length:
                particle['trail'].pop(0)
                
    def plot_particles(self, ax):
        """Plot current particle positions and trails."""
        for particle in self.particles:
            if len(particle['trail']) > 1:
                trail = np.array(particle['trail'])
                ax.plot(trail[:, 0], trail[:, 1], 
                       color=particle['color'], alpha=0.5, linewidth=1)
                       
            pos = particle['position']
            ax.scatter(pos[0], pos[1], 
                      color=particle['color'], s=particle['size'], alpha=0.8)


class ColorMaps:
    """Predefined colormaps for different physics quantities."""
    
    TEMPERATURE = 'hot'
    ELECTRIC_FIELD = 'RdBu'
    MAGNETIC_FIELD = 'viridis'
    WAVE_AMPLITUDE = 'seismic'
    PROBABILITY = 'Blues'
    ENERGY = 'plasma'
    
    @staticmethod
    def get_colormap(quantity: str) -> str:
        """Get appropriate colormap for a physics quantity."""
        mappings = {
            'temperature': ColorMaps.TEMPERATURE,
            'electric': ColorMaps.ELECTRIC_FIELD,
            'magnetic': ColorMaps.MAGNETIC_FIELD,
            'wave': ColorMaps.WAVE_AMPLITUDE,
            'probability': ColorMaps.PROBABILITY,
            'energy': ColorMaps.ENERGY
        }
        return mappings.get(quantity.lower(), 'viridis')


def create_3d_axes(figsize: Tuple[float, float] = (10, 8)):
    """Create 3D axes for 3D visualizations."""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    return fig, ax


def setup_physics_plot(title: str, xlabel: str, ylabel: str, 
                      xlim: Optional[Tuple[float, float]] = None,
                      ylim: Optional[Tuple[float, float]] = None,
                      grid: bool = True, figsize: Tuple[float, float] = (10, 6)):
    """Set up a standard physics plot with proper formatting."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
        
    if grid:
        ax.grid(True, alpha=0.3)
        
    return fig, ax


class AnimationControls:
    """Standard animation controls (play/pause/reset)."""
    
    def __init__(self, animation_obj: PhysicsAnimation):
        self.animation = animation_obj
        self.fig = animation_obj.fig
        
        # Add control buttons
        ax_play = plt.axes([0.7, 0.02, 0.08, 0.04])
        ax_pause = plt.axes([0.79, 0.02, 0.08, 0.04])
        ax_reset = plt.axes([0.88, 0.02, 0.08, 0.04])
        
        self.btn_play = Button(ax_play, 'Play')
        self.btn_pause = Button(ax_pause, 'Pause')
        self.btn_reset = Button(ax_reset, 'Reset')
        
        self.btn_play.on_clicked(self.play)
        self.btn_pause.on_clicked(self.pause)
        self.btn_reset.on_clicked(self.reset)
        
    def play(self, event):
        """Start animation."""
        if not self.animation.is_running:
            self.animation.start_animation()
            
    def pause(self, event):
        """Pause animation."""
        self.animation.stop_animation()
        
    def reset(self, event):
        """Reset animation to beginning."""
        self.animation.stop_animation()
        self.animation.init_plot()
        self.fig.canvas.draw()