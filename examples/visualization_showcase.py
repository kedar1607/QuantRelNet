"""Comprehensive showcase of all physics visualizations.

This script demonstrates the full range of physics simulations available
in the QuantRelNet library. Each visualization can be run independently
or as part of an interactive menu system.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Callable, Optional

# Import all visualization modules
from physlib.s01_classical_mechanics.visualizations import *
from physlib.s02_thermodynamics.visualizations import *
from physlib.s03_electromagnetism.visualizations import *
from physlib.s04_waves_optics.visualizations import * 
from physlib.s05_relativity.visualizations import *
from physlib.s06_quantum_mechanics.visualizations import *
from physlib.s07_astrophysics.visualizations import *


class PhysicsVisualizationShowcase:
    """Interactive showcase of all physics visualizations."""
    
    def __init__(self):
        self.demonstrations = self.setup_demonstrations()
        
    def setup_demonstrations(self) -> Dict[str, Dict[str, Callable]]:
        """Set up all available demonstrations organized by physics topic."""
        return {
            "Classical Mechanics": {
                "Projectile Motion": demo_projectile,
                "Pendulum": demo_pendulum,
                "Spring-Mass System": demo_spring_mass,
                "Particle Collisions": demo_collision,
                "Orbital Motion": lambda: create_orbital_motion_demo().show()
            },
            "Thermodynamics": {
                "Gas Particle Simulation": demo_gas_particles,
                "Heat Diffusion": demo_heat_diffusion,
                "Carnot Cycle": demo_carnot_cycle,
                "Otto Cycle": demo_otto_cycle,
                "Entropy Concepts": demo_entropy
            },
            "Electromagnetism": {
                "Electric Fields": demo_electric_fields,
                "Charged Particle Motion": demo_particle_motion,
                "Electromagnetic Waves": demo_em_wave,
                "3D EM Wave": demo_em_wave_3d,
                "Lorentz Force": demo_lorentz_force
            },
            "Waves & Optics": {
                "Wave Interference": demo_wave_interference,
                "Double-Slit Experiment": demo_double_slit,
                "Reflection & Refraction": demo_reflection_refraction,
                "Diffraction": demo_diffraction,
                "Wave Superposition": demo_wave_superposition
            },
            "Relativity": {
                "Spacetime Diagrams": demo_spacetime_diagrams,
                "Relativistic Motion": demo_relativistic_motion,
                "Twin Paradox": demo_twin_paradox,
                "Gravitational Lensing": demo_gravitational_lensing,
                "Black Holes": demo_black_holes,
                "Velocity Addition": demo_velocity_addition
            },
            "Quantum Mechanics": {
                "Wave Packet Evolution": demo_wave_packet,
                "Quantum Tunneling": demo_tunneling,
                "Harmonic Oscillator": demo_harmonic_oscillator,
                "Uncertainty Principle": demo_uncertainty_principle,
                "Quantum Measurement": demo_quantum_measurement
            },
            "Astrophysics": {
                "Cosmic Expansion": demo_cosmic_expansion,
                "Black Hole Accretion": demo_black_hole_accretion,
                "Cosmic Microwave Background": demo_cmb,
                "Stellar Evolution": demo_stellar_evolution,
                "Galaxy Collision": demo_galaxy_collision
            }
        }
    
    def display_menu(self):
        """Display interactive menu for selecting demonstrations."""
        print("\n" + "="*60)
        print("🌌 QUANTRELNET PHYSICS VISUALIZATION SHOWCASE 🌌")
        print("="*60)
        print("\nAvailable Physics Topics:")
        
        topics = list(self.demonstrations.keys())
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")
        
        print(f"{len(topics) + 1}. Run All Demonstrations")
        print(f"{len(topics) + 2}. Custom Multi-Physics Demo")
        print("0. Exit")
        
        return topics
    
    def display_topic_menu(self, topic: str):
        """Display menu for a specific physics topic."""
        print(f"\n📖 {topic.upper()} DEMONSTRATIONS")
        print("-" * 50)
        
        demos = list(self.demonstrations[topic].keys())
        for i, demo in enumerate(demos, 1):
            print(f"{i}. {demo}")
        
        print(f"{len(demos) + 1}. Run All {topic} Demos")
        print("0. Back to Main Menu")
        
        return demos
    
    def run_demo_safely(self, demo_func: Callable, demo_name: str):
        """Run a demonstration with error handling."""
        try:
            print(f"\n🚀 Starting: {demo_name}")
            print("Close the plot window to continue...")
            demo_func()
            print(f"✅ Completed: {demo_name}")
        except Exception as e:
            print(f"❌ Error in {demo_name}: {str(e)}")
            print("   This demo may require additional dependencies.")
    
    def run_topic_demos(self, topic: str):
        """Run all demonstrations for a specific topic."""
        print(f"\n🎯 Running all {topic} demonstrations...")
        for demo_name, demo_func in self.demonstrations[topic].items():
            self.run_demo_safely(demo_func, demo_name)
    
    def run_all_demos(self):
        """Run all available demonstrations."""
        print("\n🎆 Running ALL physics demonstrations!")
        print("This will take several minutes. Press Ctrl+C to interrupt.")
        
        for topic in self.demonstrations:
            print(f"\n📚 Starting {topic} section...")
            self.run_topic_demos(topic)
    
    def create_custom_multi_physics_demo(self):
        """Create a custom demonstration combining multiple physics concepts."""
        print("\n🎨 Creating Custom Multi-Physics Demonstration...")
        
        # Example: Combined classical-quantum demonstration
        try:
            from physlib.visualization import setup_physics_plot
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Multi-Physics Showcase: Classical to Quantum', fontsize=16, fontweight='bold')
            
            # Classical pendulum
            ax1 = axes[0, 0]
            t = np.linspace(0, 4*np.pi, 200)
            theta = 0.5 * np.cos(t)  # Simple harmonic motion
            ax1.plot(t, theta, 'b-', linewidth=2, label='Classical Pendulum')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Angle (rad)')
            ax1.set_title('Classical Harmonic Motion')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Wave interference
            ax2 = axes[0, 1]
            x = np.linspace(-10, 10, 200)
            wave1 = np.sin(x)
            wave2 = np.sin(x + np.pi/4)
            superposition = wave1 + wave2
            ax2.plot(x, wave1, 'b--', alpha=0.7, label='Wave 1')
            ax2.plot(x, wave2, 'r--', alpha=0.7, label='Wave 2')
            ax2.plot(x, superposition, 'purple', linewidth=2, label='Superposition')
            ax2.set_xlabel('Position')
            ax2.set_ylabel('Amplitude')
            ax2.set_title('Wave Superposition')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Quantum harmonic oscillator
            ax3 = axes[1, 0]
            x_q = np.linspace(-4, 4, 200)
            psi_0 = np.exp(-x_q**2/2) / (np.pi**0.25)  # Ground state
            psi_1 = np.sqrt(2) * x_q * np.exp(-x_q**2/2) / (np.pi**0.25)  # First excited state
            ax3.plot(x_q, psi_0, 'b-', linewidth=2, label='n=0 (ground)')
            ax3.plot(x_q, psi_1, 'r-', linewidth=2, label='n=1 (excited)')
            ax3.plot(x_q, 0.5*x_q**2, 'k--', alpha=0.5, label='Potential')
            ax3.set_xlabel('Position')
            ax3.set_ylabel('Wave Function')
            ax3.set_title('Quantum Harmonic Oscillator')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Cosmic expansion
            ax4 = axes[1, 1]
            distances = np.linspace(10, 100, 50)
            velocities = 70 * distances  # Hubble's law
            ax4.plot(distances, velocities, 'ro', markersize=4, alpha=0.7, label='Galaxies')
            ax4.plot(distances, velocities, 'b-', linewidth=2, label='Hubble\'s Law')
            ax4.set_xlabel('Distance (Mpc)')
            ax4.set_ylabel('Recession Velocity (km/s)')
            ax4.set_title('Cosmic Expansion')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
            print("✅ Custom multi-physics demonstration completed!")
            
        except Exception as e:
            print(f"❌ Error creating custom demo: {str(e)}")
    
    def run_interactive_menu(self):
        """Run the interactive menu system."""
        while True:
            topics = self.display_menu()
            
            try:
                choice = input(f"\nEnter your choice (0-{len(topics) + 2}): ").strip()
                
                if choice == '0':
                    print("👋 Thank you for exploring physics with QuantRelNet!")
                    break
                
                elif choice.isdigit():
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(topics):
                        # Selected a specific topic
                        topic = topics[choice_num - 1]
                        
                        while True:
                            demos = self.display_topic_menu(topic)
                            
                            try:
                                demo_choice = input(f"\nEnter your choice (0-{len(demos) + 1}): ").strip()
                                
                                if demo_choice == '0':
                                    break
                                
                                elif demo_choice.isdigit():
                                    demo_num = int(demo_choice)
                                    
                                    if 1 <= demo_num <= len(demos):
                                        # Run specific demo
                                        demo_name = demos[demo_num - 1]
                                        demo_func = self.demonstrations[topic][demo_name]
                                        self.run_demo_safely(demo_func, demo_name)
                                        
                                    elif demo_num == len(demos) + 1:
                                        # Run all demos in topic
                                        self.run_topic_demos(topic)
                                        
                                    else:
                                        print("❌ Invalid choice. Please try again.")
                                        
                                else:
                                    print("❌ Please enter a number.")
                                    
                            except KeyboardInterrupt:
                                print("\n⏸️  Interrupted by user.")
                                break
                            except Exception as e:
                                print(f"❌ Error: {str(e)}")
                    
                    elif choice_num == len(topics) + 1:
                        # Run all demonstrations
                        confirm = input("This will run ALL demonstrations. Continue? (y/N): ").strip().lower()
                        if confirm in ['y', 'yes']:
                            self.run_all_demos()
                    
                    elif choice_num == len(topics) + 2:
                        # Custom multi-physics demo
                        self.create_custom_multi_physics_demo()
                    
                    else:
                        print("❌ Invalid choice. Please try again.")
                
                else:
                    print("❌ Please enter a number.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def quick_demo_tour():
    """Quick tour of key demonstrations from each physics area."""
    print("🎯 QUICK PHYSICS TOUR - Key Demonstrations")
    print("="*50)
    
    showcase = PhysicsVisualizationShowcase()
    
    # Select one key demo from each area
    key_demos = [
        ("Classical Mechanics", "Pendulum", demo_pendulum),
        ("Thermodynamics", "Gas Particle Simulation", demo_gas_particles),
        ("Electromagnetism", "Electric Fields", demo_electric_fields),
        ("Waves & Optics", "Double-Slit Experiment", demo_double_slit),
        ("Relativity", "Spacetime Diagrams", demo_spacetime_diagrams),
        ("Quantum Mechanics", "Wave Packet Evolution", demo_wave_packet),
        ("Astrophysics", "Cosmic Expansion", demo_cosmic_expansion)
    ]
    
    for topic, demo_name, demo_func in key_demos:
        print(f"\n📖 {topic}: {demo_name}")
        showcase.run_demo_safely(demo_func, demo_name)
    
    print("\n✅ Quick tour completed!")


def physics_concept_comparison():
    """Compare related concepts across different physics domains."""
    print("🔬 PHYSICS CONCEPT COMPARISON")
    print("="*40)
    
    try:
        # Compare waves across different domains
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Wave Phenomena Across Physics', fontsize=16, fontweight='bold')
        
        x = np.linspace(0, 4*np.pi, 200)
        
        # Classical wave
        axes[0, 0].plot(x, np.sin(x), 'b-', linewidth=2, label='y = sin(x)')
        axes[0, 0].set_title('Classical Wave')
        axes[0, 0].set_xlabel('Position')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Electromagnetic wave
        axes[0, 1].plot(x, np.sin(x), 'r-', linewidth=2, label='E-field')
        axes[0, 1].plot(x, np.cos(x), 'b-', linewidth=2, label='B-field')
        axes[0, 1].set_title('Electromagnetic Wave')
        axes[0, 1].set_xlabel('Position')
        axes[0, 1].set_ylabel('Field Amplitude')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Quantum wave function
        axes[0, 2].plot(x, np.sin(x), 'purple', linewidth=2, label='Re(ψ)')
        axes[0, 2].plot(x, np.cos(x), 'orange', linewidth=2, label='Im(ψ)')
        axes[0, 2].plot(x, np.sin(x)**2 + np.cos(x)**2, 'k--', linewidth=2, label='|ψ|²')
        axes[0, 2].set_title('Quantum Wave Function')
        axes[0, 2].set_xlabel('Position')
        axes[0, 2].set_ylabel('Amplitude')
        axes[0, 2].legend()
        axes[0, 2].grid(True, alpha=0.3)
        
        # Oscillators comparison
        t = np.linspace(0, 4*np.pi, 200)
        
        # Classical oscillator
        axes[1, 0].plot(t, np.cos(t), 'g-', linewidth=2, label='Position')
        axes[1, 0].plot(t, -np.sin(t), 'r-', linewidth=2, label='Velocity')
        axes[1, 0].set_title('Classical Harmonic Oscillator')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Amplitude')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # LC circuit (electromagnetic oscillator)
        axes[1, 1].plot(t, np.cos(t), 'b-', linewidth=2, label='Charge')
        axes[1, 1].plot(t, -np.sin(t), 'r-', linewidth=2, label='Current')
        axes[1, 1].set_title('LC Circuit Oscillation')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Amplitude')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        # Quantum oscillator (probability evolution)
        # Superposition of ground and first excited state
        psi_superposition = 0.5 * (np.cos(0.5*t) + np.cos(1.5*t))
        axes[1, 2].plot(t, psi_superposition**2, 'purple', linewidth=2, label='|ψ(t)|²')
        axes[1, 2].set_title('Quantum Oscillator (Coherent State)')
        axes[1, 2].set_xlabel('Time')
        axes[1, 2].set_ylabel('Probability Density')
        axes[1, 2].legend()
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Physics concept comparison completed!")
        
    except Exception as e:
        print(f"❌ Error creating comparison: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            quick_demo_tour()
        elif sys.argv[1] == "--compare":
            physics_concept_comparison()
        elif sys.argv[1] == "--custom":
            showcase = PhysicsVisualizationShowcase()
            showcase.create_custom_multi_physics_demo()
        else:
            print("Usage: python visualization_showcase.py [--quick|--compare|--custom]")
    else:
        # Run interactive menu
        showcase = PhysicsVisualizationShowcase()
        showcase.run_interactive_menu()