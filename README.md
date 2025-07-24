# QuantRelNet

A modular Python library for exploring fundamental physics concepts.

This project provides a collection of small utilities covering classical mechanics, thermodynamics, electromagnetism, waves and optics, relativity, quantum mechanics and astrophysics. Each concept is organised into its own package with simple classes and functions.

The code is intentionally lightweight so newcomers can read and modify it easily. See `examples/main.py` for a quick demonstration of how to use the library.

## Structure

```
physlib/
    classical_mechanics/
    thermodynamics/
    electromagnetism/
    waves_optics/
    relativity/
    quantum_mechanics/
    astrophysics/
```

Each package contains modules implementing key formulas. Functions in one package may call functions from others when the physics requires it. For example `work_done` in `energy.py` uses the `force` function from `newton.py` because work is defined in terms of force and distance.

The library can serve as a starting point for building animations or simulations to visualise physics in 3D environments.

## Example usage

Run the example script after installing the project in editable mode:

```bash
python -m pip install -e .[examples]
python examples/main.py
```

This prints values computed from several modules:

- Newton's laws are used to compute acceleration and kinetic energy.
- The first law of thermodynamics calculates work from internal energy change and heat.
- The Lorentz force demonstrates basic electromagnetism.
- A sample sine wave is generated from the wave equation utilities.
- Special relativity shows time dilation for a moving object.
- The uncertainty principle helper checks if given uncertainties satisfy Heisenberg's bound.

Each function is documented with the formula it implements so learners can connect the code to the underlying physics.
