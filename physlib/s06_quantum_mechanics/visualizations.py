"""Visual simulations for quantum mechanics concepts."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
from typing import List, Tuple, Optional, Callable
from ..visualization import PhysicsAnimation, setup_physics_plot, ColorMaps, InteractivePhysicsPlot
from . import schrodinger, tunneling, uncertainty


class QuantumWavePacket(PhysicsAnimation):
    """Animate quantum wave packet evolution."""
    
    def __init__(self, initial_position: float = -3.0, initial_momentum: float = 2.0,
                 sigma: float = 0.5, figsize=(12, 8)):
        super().__init__(figsize)
        self.x0 = initial_position
        self.k0 = initial_momentum  # Initial momentum (ħk)
        self.sigma = sigma
        self.dt = 0.01
        self.hbar = 1.0  # Set ħ = 1 for convenience
        self.m = 1.0     # Particle mass
        
        # Spatial grid
        self.x = np.linspace(-10, 10, 400)
        self.dx = self.x[1] - self.x[0]
        
        # Create subplots
        self.fig.clear()
        self.ax_wavefunction = self.fig.add_subplot(211)
        self.ax_probability = self.fig.add_subplot(212)
        
        # Plot elements
        self.psi_real_line, = self.ax_wavefunction.plot([], [], 'b-', linewidth=2, label='Re(ψ)')
        self.psi_imag_line, = self.ax_wavefunction.plot([], [], 'r-', linewidth=2, label='Im(ψ)')
        self.prob_line, = self.ax_probability.plot([], [], 'purple', linewidth=3, label='|ψ|²')
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Wave function plot
        self.ax_wavefunction.set_xlim(-10, 10)
        self.ax_wavefunction.set_ylim(-1, 1)
        self.ax_wavefunction.set_ylabel('Wave Function')
        self.ax_wavefunction.set_title('Quantum Wave Packet Evolution')
        self.ax_wavefunction.legend()
        self.ax_wavefunction.grid(True, alpha=0.3)
        
        # Probability density plot
        self.ax_probability.set_xlim(-10, 10)
        self.ax_probability.set_ylim(0, 1)
        self.ax_probability.set_xlabel('Position')
        self.ax_probability.set_ylabel('Probability Density')
        self.ax_probability.legend()
        self.ax_probability.grid(True, alpha=0.3)
        
        # Add time display
        self.time_text = self.ax_wavefunction.text(0.02, 0.95, '', transform=self.ax_wavefunction.transAxes,
                                                  fontsize=12, verticalalignment='top',
                                                  bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
    def gaussian_wave_packet(self, x: np.ndarray, t: float) -> np.ndarray:
        """Calculate Gaussian wave packet at time t."""
        # Time-dependent width
        sigma_t = self.sigma * np.sqrt(1 + (self.hbar * t / (self.m * self.sigma**2))**2)
        
        # Phase factors
        phase_classical = self.k0 * (self.x0 + self.hbar * self.k0 * t / self.m) - (self.hbar * self.k0**2 * t) / (2 * self.m)
        phase_dispersion = np.arctan(self.hbar * t / (self.m * self.sigma**2))
        
        # Position of wave packet center
        x_center = self.x0 + self.hbar * self.k0 * t / self.m
        
        # Gaussian envelope
        envelope = (2 * np.pi * sigma_t**2)**(-0.25) * np.exp(-(x - x_center)**2 / (4 * sigma_t**2))
        
        # Full wave function
        psi = envelope * np.exp(1j * (self.k0 * x - phase_classical - phase_dispersion/2))
        
        return psi
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.psi_real_line, self.psi_imag_line, self.prob_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * self.dt
        
        # Calculate wave function
        psi = self.gaussian_wave_packet(self.x, t)
        psi_real = np.real(psi)
        psi_imag = np.imag(psi)
        probability = np.abs(psi)**2
        
        # Update plots
        self.psi_real_line.set_data(self.x, psi_real)
        self.psi_imag_line.set_data(self.x, psi_imag)
        self.prob_line.set_data(self.x, probability)
        
        # Update time display
        self.time_text.set_text(f't = {t:.2f}')
        
        return [self.psi_real_line, self.psi_imag_line, self.prob_line]


class QuantumTunneling(PhysicsAnimation):
    """Visualize quantum tunneling through potential barriers."""
    
    def __init__(self, barrier_height: float = 2.0, barrier_width: float = 1.0,
                 particle_energy: float = 1.0, figsize=(12, 8)):
        super().__init__(figsize)
        self.V0 = barrier_height
        self.barrier_width = barrier_width
        self.E = particle_energy
        self.dt = 0.02
        
        # Spatial grid
        self.x = np.linspace(-8, 8, 400)
        self.dx = self.x[1] - self.x[0]
        
        # Barrier position
        self.barrier_start = -barrier_width/2
        self.barrier_end = barrier_width/2
        
        # Wave parameters
        self.hbar = 1.0
        self.m = 1.0
        self.k = np.sqrt(2 * self.m * self.E) / self.hbar
        
        # Create subplots
        self.fig.clear()
        self.ax_potential = self.fig.add_subplot(211)
        self.ax_wavefunction = self.fig.add_subplot(212)
        
        # Plot elements
        self.potential_line, = self.ax_potential.plot([], [], 'k-', linewidth=3, label='Potential V(x)')
        self.energy_line, = self.ax_potential.plot([], [], 'r--', linewidth=2, label=f'Particle Energy = {self.E}')
        
        self.psi_real_line, = self.ax_wavefunction.plot([], [], 'b-', linewidth=2, label='Re(ψ)')
        self.psi_imag_line, = self.ax_wavefunction.plot([], [], 'r-', linewidth=2, label='Im(ψ)')
        self.prob_line, = self.ax_wavefunction.plot([], [], 'purple', linewidth=3, alpha=0.7, label='|ψ|²')
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Potential plot
        self.ax_potential.set_xlim(-8, 8)
        self.ax_potential.set_ylim(0, max(3, self.V0 * 1.2))
        self.ax_potential.set_ylabel('Energy')
        self.ax_potential.set_title('Quantum Tunneling')
        self.ax_potential.legend()
        self.ax_potential.grid(True, alpha=0.3)
        
        # Wave function plot
        self.ax_wavefunction.set_xlim(-8, 8)
        self.ax_wavefunction.set_ylim(-2, 2)
        self.ax_wavefunction.set_xlabel('Position')
        self.ax_wavefunction.set_ylabel('Wave Function')
        self.ax_wavefunction.legend()
        self.ax_wavefunction.grid(True, alpha=0.3)
        
        # Draw potential barrier
        potential = self.create_potential()
        self.potential_line.set_data(self.x, potential)
        self.energy_line.set_data(self.x, np.full_like(self.x, self.E))
        
        # Add barrier shading
        self.ax_potential.axvspan(self.barrier_start, self.barrier_end, 
                                 alpha=0.3, color='gray', label='Barrier')
        self.ax_wavefunction.axvspan(self.barrier_start, self.barrier_end, 
                                    alpha=0.2, color='gray')
        
    def create_potential(self) -> np.ndarray:
        """Create the potential barrier."""
        potential = np.zeros_like(self.x)
        barrier_mask = (self.x >= self.barrier_start) & (self.x <= self.barrier_end)
        potential[barrier_mask] = self.V0
        return potential
        
    def calculate_transmission_coefficient(self) -> float:
        """Calculate quantum tunneling transmission coefficient."""
        if self.E >= self.V0:
            return 1.0  # Classical case - particle goes over barrier
        
        # Quantum tunneling case
        kappa = np.sqrt(2 * self.m * (self.V0 - self.E)) / self.hbar
        T = 1 / (1 + (self.V0**2 * np.sinh(kappa * self.barrier_width)**2) / (4 * self.E * (self.V0 - self.E)))
        return T
        
    def wave_function_solution(self, t: float) -> np.ndarray:
        """Calculate wave function for tunneling problem."""
        psi = np.zeros_like(self.x, dtype=complex)
        
        # Wave numbers
        k1 = np.sqrt(2 * self.m * self.E) / self.hbar  # Outside barrier
        
        if self.E < self.V0:
            k2 = 1j * np.sqrt(2 * self.m * (self.V0 - self.E)) / self.hbar  # Inside barrier (evanescent)
        else:
            k2 = np.sqrt(2 * self.m * (self.E - self.V0)) / self.hbar  # Inside barrier (propagating)
        
        # Transmission coefficient
        T = self.calculate_transmission_coefficient()
        
        # Incident wave packet (Gaussian)
        x_center = -4 + 2 * t  # Moving wave packet
        sigma = 0.5
        
        for i, x_pos in enumerate(self.x):
            if x_pos < self.barrier_start:
                # Region I: Incident + reflected wave
                incident = np.exp(1j * k1 * x_pos) * np.exp(-(x_pos - x_center)**2 / (2 * sigma**2))
                reflected = (1 - T) * np.exp(-1j * k1 * x_pos) * np.exp(-(x_pos - x_center)**2 / (2 * sigma**2))
                psi[i] = incident + reflected
                
            elif x_pos <= self.barrier_end:
                # Region II: Inside barrier
                if self.E < self.V0:
                    # Evanescent wave
                    decay_factor = np.exp(-np.real(k2) * (x_pos - self.barrier_start))
                    psi[i] = np.sqrt(T) * decay_factor * np.exp(-(x_center - self.barrier_start)**2 / (2 * sigma**2))
                else:
                    # Propagating wave inside barrier
                    psi[i] = np.sqrt(T) * np.exp(1j * k2 * x_pos) * np.exp(-(x_center - self.barrier_start)**2 / (2 * sigma**2))
                    
            else:
                # Region III: Transmitted wave
                transmitted = np.sqrt(T) * np.exp(1j * k1 * x_pos) * np.exp(-(x_center - self.barrier_end)**2 / (2 * sigma**2))
                psi[i] = transmitted
        
        # Apply time evolution
        psi *= np.exp(-1j * self.E * t / self.hbar)
        
        return psi
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return [self.potential_line, self.energy_line, self.psi_real_line, self.psi_imag_line, self.prob_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * self.dt
        
        # Calculate wave function
        psi = self.wave_function_solution(t)
        psi_real = np.real(psi)
        psi_imag = np.imag(psi)
        probability = np.abs(psi)**2
        
        # Update wave function plots
        self.psi_real_line.set_data(self.x, psi_real)
        self.psi_imag_line.set_data(self.x, psi_imag)
        self.prob_line.set_data(self.x, probability)
        
        return [self.potential_line, self.energy_line, self.psi_real_line, self.psi_imag_line, self.prob_line]


class QuantumHarmonicOscillator(PhysicsAnimation):
    """Visualize quantum harmonic oscillator eigenstates."""
    
    def __init__(self, n_max: int = 4, figsize=(12, 10)):
        super().__init__(figsize)
        self.n_max = n_max
        self.omega = 1.0  # Oscillator frequency
        self.hbar = 1.0
        self.m = 1.0
        
        # Spatial grid
        self.x = np.linspace(-4, 4, 300)
        
        # Create subplots
        self.fig.clear()
        self.ax_states = self.fig.add_subplot(211)
        self.ax_evolution = self.fig.add_subplot(212)
        
        # Plot elements for individual states
        self.state_lines = []
        self.prob_lines = []
        
        # Plot elements for time evolution  
        self.evolved_real_line, = self.ax_evolution.plot([], [], 'b-', linewidth=2, label='Re(ψ)')
        self.evolved_imag_line, = self.ax_evolution.plot([], [], 'r-', linewidth=2, label='Im(ψ)')
        self.evolved_prob_line, = self.ax_evolution.plot([], [], 'purple', linewidth=3, label='|ψ|²')
        
        self.setup_plot()
        
    def setup_plot(self):
        """Configure plot appearance."""
        # Individual states plot
        self.ax_states.set_xlim(-4, 4)
        self.ax_states.set_ylim(0, 4)
        self.ax_states.set_ylabel('Energy + Wave Function')
        self.ax_states.set_title('Quantum Harmonic Oscillator Eigenstates')
        self.ax_states.grid(True, alpha=0.3)
        
        # Time evolution plot
        self.ax_evolution.set_xlim(-4, 4)
        self.ax_evolution.set_ylim(-2, 2)
        self.ax_evolution.set_xlabel('Position')
        self.ax_evolution.set_ylabel('Wave Function')
        self.ax_evolution.set_title('Superposition State Evolution')
        self.ax_evolution.legend()
        self.ax_evolution.grid(True, alpha=0.3)
        
        # Plot potential
        V = 0.5 * self.m * self.omega**2 * self.x**2
        self.ax_states.plot(self.x, V, 'k-', linewidth=2, label='Potential V(x)')
        
        # Plot energy levels and eigenstates
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        for n in range(self.n_max + 1):
            energy = self.hbar * self.omega * (n + 0.5)
            
            # Energy level line
            self.ax_states.axhline(energy, color='gray', linestyle='--', alpha=0.5)
            
            # Eigenstate
            psi_n = self.harmonic_oscillator_eigenstate(n)
            
            # Plot shifted by energy level
            line, = self.ax_states.plot(self.x, energy + psi_n, colors[n % len(colors)], 
                                       linewidth=2, label=f'n={n}')
            self.state_lines.append(line)
            
        self.ax_states.legend()
        
    def harmonic_oscillator_eigenstate(self, n: int) -> np.ndarray:
        """Calculate the nth eigenstate of quantum harmonic oscillator."""
        # Characteristic length
        x0 = np.sqrt(self.hbar / (self.m * self.omega))
        
        # Dimensionless coordinate
        xi = self.x / x0
        
        # Hermite polynomials (first few)
        hermite_polys = {
            0: np.ones_like(xi),
            1: 2 * xi,
            2: 4 * xi**2 - 2,
            3: 8 * xi**3 - 12 * xi,
            4: 16 * xi**4 - 48 * xi**2 + 12
        }
        
        if n > 4:
            # Use recurrence relation for higher n
            H_n = hermite_polys[4]  # Fallback
        else:
            H_n = hermite_polys[n]
        
        # Normalization constant
        norm = (self.m * self.omega / (np.pi * self.hbar))**(1/4) / np.sqrt(2**n * np.math.factorial(n))
        
        # Complete eigenstate
        psi_n = norm * H_n * np.exp(-xi**2 / 2)
        
        return psi_n
        
    def superposition_state(self, t: float) -> np.ndarray:
        """Create a superposition of eigenstates that evolves in time."""
        # Coherent state (closest quantum analog to classical oscillator)
        alpha = 2.0  # Coherent state parameter
        
        psi_total = np.zeros_like(self.x, dtype=complex)
        
        for n in range(self.n_max + 1):
            # Coherent state coefficients
            c_n = np.exp(-abs(alpha)**2 / 2) * (alpha**n) / np.sqrt(np.math.factorial(n))
            
            # Time evolution phase
            energy = self.hbar * self.omega * (n + 0.5)
            phase = np.exp(-1j * energy * t / self.hbar)
            
            # Add to superposition
            psi_n = self.harmonic_oscillator_eigenstate(n)
            psi_total += c_n * phase * psi_n
            
        return psi_total
        
    def init_plot(self) -> List:
        """Initialize animation elements."""
        return self.state_lines + [self.evolved_real_line, self.evolved_imag_line, self.evolved_prob_line]
        
    def animate(self, frame: int) -> List:
        """Update animation frame."""
        t = frame * 0.1
        
        # Calculate superposition state
        psi = self.superposition_state(t)
        psi_real = np.real(psi)
        psi_imag = np.imag(psi)
        probability = np.abs(psi)**2
        
        # Update evolution plots
        self.evolved_real_line.set_data(self.x, psi_real)
        self.evolved_imag_line.set_data(self.x, psi_imag)
        self.evolved_prob_line.set_data(self.x, probability)
        
        return self.state_lines + [self.evolved_real_line, self.evolved_imag_line, self.evolved_prob_line]


class UncertaintyPrincipleDemo:
    """Demonstrate the Heisenberg uncertainty principle."""
    
    def __init__(self, figsize=(12, 8)):
        self.fig, self.axes = plt.subplots(2, 2, figsize=figsize)
        self.axes = self.axes.flatten()
        
    def plot_position_momentum_uncertainty(self, ax, sigma_x: float = 1.0):
        """Plot wave packets with different position uncertainties."""
        x = np.linspace(-6, 6, 300)
        
        # Different width wave packets
        sigmas = [0.5, 1.0, 2.0]
        colors = ['blue', 'red', 'green']
        
        for sigma, color in zip(sigmas, colors):
            # Position wave function (Gaussian)
            psi_x = np.exp(-x**2 / (2 * sigma**2)) / (2 * np.pi * sigma**2)**(1/4)
            
            # Corresponding momentum uncertainty (Δp = ħ/(2Δx))
            delta_p = 1.0 / (2 * sigma)  # ħ = 1
            
            ax.plot(x, psi_x, color=color, linewidth=2, 
                   label=f'Δx = {sigma:.1f}, Δp = {delta_p:.2f}')
            
        ax.set_xlabel('Position')
        ax.set_ylabel('Wave Function |ψ(x)|')
        ax.set_title('Position-Momentum Uncertainty Trade-off')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_uncertainty_product(self, ax):
        """Plot the uncertainty product ΔxΔp."""
        sigma_x_values = np.linspace(0.2, 3.0, 100)
        delta_p_values = 1.0 / (2 * sigma_x_values)  # ħ = 1
        uncertainty_product = sigma_x_values * delta_p_values
        
        ax.plot(sigma_x_values, uncertainty_product, 'purple', linewidth=3, 
               label='ΔxΔp')
        ax.axhline(0.5, color='red', linestyle='--', linewidth=2, 
                  label='Minimum (ħ/2)')
        
        ax.set_xlabel('Position Uncertainty Δx')
        ax.set_ylabel('Uncertainty Product ΔxΔp')
        ax.set_title('Heisenberg Uncertainty Principle')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_energy_time_uncertainty(self, ax):
        """Plot energy-time uncertainty relation."""
        # Excited state lifetime vs energy uncertainty
        lifetimes = np.logspace(-15, -10, 100)  # seconds
        energy_uncertainties = 6.582e-16 / lifetimes  # ΔE = ħ/Δt in eV
        
        ax.loglog(lifetimes * 1e12, energy_uncertainties, 'orange', linewidth=3,
                 label='ΔEΔt = ħ')
        
        # Mark some typical atomic processes
        ax.scatter([1e-3], [0.66], s=100, c='red', zorder=5, label='Optical transition')
        ax.scatter([1e3], [6.6e-7], s=100, c='blue', zorder=5, label='Nuclear decay')
        
        ax.set_xlabel('Lifetime Δt (ps)')
        ax.set_ylabel('Energy Uncertainty ΔE (eV)')
        ax.set_title('Energy-Time Uncertainty')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_measurement_disturbance(self, ax):
        """Illustrate measurement disturbance in quantum mechanics."""
        # Photon momentum vs wavelength for position measurement
        wavelengths = np.linspace(100e-9, 1000e-9, 100)  # nm
        photon_momenta = 6.626e-34 / wavelengths  # p = h/λ
        
        # Position resolution (diffraction limit)
        position_resolution = wavelengths / 2  # Approximate
        
        ax.plot(wavelengths * 1e9, position_resolution * 1e9, 'blue', linewidth=2,
               label='Position Resolution')
        
        # Secondary y-axis for momentum disturbance
        ax2 = ax.twinx()
        ax2.plot(wavelengths * 1e9, photon_momenta * 1e24, 'red', linewidth=2,
                label='Photon Momentum')
        
        ax.set_xlabel('Photon Wavelength (nm)')
        ax.set_ylabel('Position Resolution (nm)', color='blue')
        ax2.set_ylabel('Photon Momentum (×10⁻²⁴ kg⋅m/s)', color='red')
        ax.set_title('Measurement Trade-off')
        
        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='center')
        
        ax.grid(True, alpha=0.3)
        
    def show(self):
        """Display all uncertainty principle demonstrations."""
        self.plot_position_momentum_uncertainty(self.axes[0])
        self.plot_uncertainty_product(self.axes[1])
        self.plot_energy_time_uncertainty(self.axes[2])
        self.plot_measurement_disturbance(self.axes[3])
        
        plt.tight_layout()
        plt.show()


def create_quantum_measurement_demo():
    """Interactive demo of quantum measurement and state collapse."""
    plot = InteractivePhysicsPlot(figsize=(12, 8))
    
    # Parameters
    params = {
        'measurement_position': 0.0,
        'measurement_uncertainty': 0.5,
        'pre_measurement': True
    }
    
    def update_measurement(val=None):
        """Update quantum measurement demonstration."""
        plot.main_ax.clear()
        
        x = np.linspace(-5, 5, 300)
        
        if params['pre_measurement']:
            # Before measurement: superposition state
            psi = (np.exp(-(x-1)**2/2) + np.exp(-(x+1)**2/2)) / np.sqrt(2)
            probability = np.abs(psi)**2
            
            plot.main_ax.plot(x, psi, 'b-', linewidth=2, label='Wave Function ψ(x)')
            plot.main_ax.plot(x, probability, 'purple', linewidth=3, alpha=0.7, label='Probability |ψ|²')
            plot.main_ax.set_title('Before Measurement: Superposition State')
            
        else:
            # After measurement: collapsed state
            x_meas = params['measurement_position']
            sigma_meas = params['measurement_uncertainty']
            
            # Collapsed wave function (Gaussian around measurement result)
            psi_collapsed = np.exp(-(x - x_meas)**2 / (2 * sigma_meas**2))
            psi_collapsed /= np.sqrt(np.trapz(psi_collapsed**2, x))  # Normalize
            
            probability = np.abs(psi_collapsed)**2
            
            plot.main_ax.plot(x, psi_collapsed, 'r-', linewidth=2, label='Collapsed ψ(x)')
            plot.main_ax.plot(x, probability, 'orange', linewidth=3, alpha=0.7, label='Post-measurement |ψ|²')
            plot.main_ax.axvline(x_meas, color='red', linestyle='--', linewidth=2, 
                               label=f'Measurement at x={x_meas:.1f}')
            plot.main_ax.set_title('After Measurement: State Collapse')
            
        plot.main_ax.set_xlim(-5, 5)
        plot.main_ax.set_ylim(-0.5, 1.5)
        plot.main_ax.set_xlabel('Position')
        plot.main_ax.set_ylabel('Amplitude')
        plot.main_ax.legend()
        plot.main_ax.grid(True, alpha=0.3)
        
        plot.fig.canvas.draw()
    
    # Add controls
    plot.add_slider('Meas. Pos.', -2.0, 2.0, params['measurement_position'],
                   lambda val: (params.update({'measurement_position': val}), update_measurement()))
    plot.add_slider('Meas. Unc.', 0.1, 1.0, params['measurement_uncertainty'],
                   lambda val: (params.update({'measurement_uncertainty': val}), update_measurement()))
    
    def toggle_measurement():
        params['pre_measurement'] = not params['pre_measurement']
        update_measurement()
        
    plot.add_button('Toggle Measurement', toggle_measurement, (3, 0))
    
    # Initial plot
    update_measurement()
    
    return plot


# Convenience functions for quick demonstrations
def demo_wave_packet():
    """Quick quantum wave packet demo."""
    sim = QuantumWavePacket(initial_position=-3, initial_momentum=3)
    sim.start_animation(interval=50, frames=400)
    sim.show()

def demo_tunneling():
    """Quick quantum tunneling demo."""
    sim = QuantumTunneling(barrier_height=3.0, barrier_width=1.5, particle_energy=2.0)
    sim.start_animation(interval=100, frames=300)
    sim.show()

def demo_harmonic_oscillator():
    """Quick quantum harmonic oscillator demo."""
    sim = QuantumHarmonicOscillator(n_max=4)
    sim.start_animation(interval=100, frames=200)
    sim.show()

def demo_uncertainty_principle():
    """Quick uncertainty principle demo."""
    demo = UncertaintyPrincipleDemo()
    demo.show()

def demo_quantum_measurement():
    """Quick quantum measurement demo."""
    demo = create_quantum_measurement_demo()
    demo.show()