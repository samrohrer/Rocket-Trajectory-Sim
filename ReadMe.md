# Rocket Trajectory Simulator

A 1D rocket flight trajectory simulator built from scratch in Python, modeling a competition vehicle flying on an **AeroTech M2500T-PS** solid motor. Independent personal project using real motor spec/thrust-curve data rather than idealized constants.

## Features

- Euler integration of 1D flight dynamics (gravity, thrust, drag)
- Real thrust curve data (AeroTech M2500T-PS) loaded from CSV, interpolated with `np.interp()`
- Variable atmospheric density model
- Impulse-based propellant mass depletion (mass loss tied to thrust output, not elapsed time)
- Full flight history tracking (time, altitude, velocity, acceleration, thrust, drag, mass)
- Multi-panel diagnostic plot with burnout/apogee event markers
- Convergence-validated timestep (`dt = 0.01s`)

## Validation

Simulator output was compared against an independently-built OpenRocket
model of the same vehicle

| Metric | Initial | Corrected | OpenRocket | Final Error |
| ------ | ------- |-----------| ---------- |-------------|
| Liftoff Mass | 26.7 kg | 30 kg     | 30.06 kg | 0.2%        |
| Burnout Velocity | 325 m/s | 265.6 m/s | 266 m/s | -0.15%      |
| Apogee | 3758 m | 2836.6 m  | 2853 m | -0.5%       |

Validation surfaced two modeling errors. One, in which the motor casing
(3.494 kg) was omitted — the model treated propellant as the entire
motor mass. Correcting this reduced apogee error from +32% to +20%. The second
was the simulation not having a launch pad, requiring an artificial 30 m/s 
initial velocity to run. Fixing that brought the apogee error with 0.5% and the 
peak velocity within 0.15% of OpenRocket.

Full methodology and resolved discrepancies:
[VALIDATION.md](VALIDATION.md)

## Architecture

```
Rocket          # Fixed vehicle/motor properties + thrust curve lookup table
Environment     # Atmospheric model (density, gravity)
FlightState     # Time-evolving simulation state + full flight history
```

## Status

Core simulation complete and validated against OpenRocket. Validation revealed mass-model error which was corrected. A drag coefficient discrepancy still remains

**Roadmap:** config-file loading → .eng motor parsing → parachute deployment → RK4 integration → Monte Carlo dispersion analysis

## Tech Stack

Python · NumPy · Matplotlib

## Usage

```bash
python main.py
```
