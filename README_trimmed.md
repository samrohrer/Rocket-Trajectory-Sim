# Rocket Trajectory Simulator

A 1D rocket flight trajectory simulator built from scratch in Python, modeling MSU Rocketry's **Spartacus MKIII** competition vehicle flying on an **AeroTech M2500T-PS** solid motor. Independent personal project using real motor spec/thrust-curve data rather than idealized constants.

## Features

- Euler integration of 1D flight dynamics (gravity, thrust, drag)
- Real thrust curve data (AeroTech M2500T-PS) loaded from CSV, interpolated with `np.interp()`
- Variable atmospheric density model
- Impulse-based propellant mass depletion (mass loss tied to thrust output, not elapsed time)
- Full flight history tracking (time, altitude, velocity, acceleration, thrust, drag, mass)
- Multi-panel diagnostic plot with burnout/apogee event markers
- Convergence-validated timestep (`dt = 0.01s`)

## Architecture

```
Rocket          # Fixed vehicle/motor properties + thrust curve lookup table
Environment     # Atmospheric model (density, gravity)
FlightState     # Time-evolving simulation state + full flight history
```

## Status

Core simulation (integration, real thrust curve, impulse-based mass depletion, diagnostics) is complete and validated against physical expectations. Next up: OpenRocket validation, then refactoring.

**Roadmap:** OpenRocket validation → refactor (fix known one-`dt` flight-time imprecision) → config-file loading → parachute deployment → Monte Carlo dispersion analysis → RK4 integration.

## Tech Stack

Python · NumPy · Matplotlib

## Usage

```bash
python main.py
```

*(Add setup/install instructions once dependencies are finalized.)*

---

For design rationale (thrust-curve vs. constant-thrust findings, convergence study, impulse-based depletion reasoning), see [`docs/design-notes.md`](docs/design-notes.md).
