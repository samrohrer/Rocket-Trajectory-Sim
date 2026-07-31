## Validation -- Python Trajectory Sim vs. OpenRocket

## Reference Model Configuration

OpenRocket model built independently from Spartacus MKIII geometry.
Comparison only valid under these settings:

Flight configuration | M2500T-0
Wind speed / turbulence | 0 m/s / 0%
Wind Direction | 0°
Launch rod angle | 0°
Launch rod length | 5 m
Atmosphere | ISA
Launch site altitude | 0 m (28.61 N, 80.6 W)
Airframe mass override | 22.0 kg (no motor)
Body tube OD | 15.2 cm

Reference Apogee: 2853 m | Peak Velocity: 266 m/s (Mach 0.786)


## Results Summary

| Metric | Initial | Corrected | OpenRocket | Final Error |
| ------ | ------- | --------- | ---------- | ----------- |
| Liftoff Mass | 26.7 kg | 30 kg | 30.06 kg | 0.2% |
| Burnout Velocity | 325 m/s | 280 m/s | 266 m/s | +7.7% |
| Apogee | 3758 m | 2857 m | 2853 m | +0.14% |
Apogee match uses a calibrated Cd and is not an independent prediction. The mass fix alone reduced error from 32% to ~20%.


## Discrepancies -- Resolved

### D1 - Motor casing omitted from mass model
Symptom: Burnout velocity 325 m/s vs OpenRocket 266 m/s
Cause: Mass model treated propellant (4.531 kg) as the entire motor. The encasing of the actual motor (3.494 kg)
       was never included
Found by: Comparing liftoff mass with OpenRocket's "mass with motors" line. Initially was looking for problems
          with drag, but came across different mass numbers
Fix: Burnout_Mass = 25.494 kg (22 kg airframe + 3.494 kg motor casing)
     Propellant_Mass = 4.531 kg (According to AeroTech motor data sheet)
Result: Liftoff mass = 30.0 kg compared to OpenRocket's 30.06 kg
        Apogee error reduced from +32% to +20% (3758m to ~3430m)

### D2 - Parachute Cd Used during Ascent
Descent Cd of 1.75 used for all phases of rocket flight, overestimating the ascent drag by roughly
3 to 4 times

### D3 - Input parameter errors
Corrected dry mass, cross sectional area, and rail departure velocity


## Open - Drag Coefficient underpredicted (Unresolved)
Symptom: After correcting D1, apogee was still about ~3400m vs. OpenRocket's 2853m
         A +20% residual with burnout velocity still ~8% high
Cause: The assumed Cd of 0.44 underpredicts the total drag. OpenRocket's component breakdown of drag coefficients
       gives friction = ~0.31, base = ~ 0.14-0.19, and pressure = ~ 0.01-0.04, summing to about 0.47-0.54. The
       calibrated result of 0.685 exceeds this sum, likely reflecting that another source of error must be the
       cause of the apogee discrepancy. The original 0.44 coefficient has an undetermined origin.
Fix: Unresolved


## Limitations
- 1D vertical only
- Cd is calibrated to this airframe (Not derived from geometry) and would not hold up against other rocket airframes
- No recovery system modeled


## Future Work:
- Config file for rocket parameters
- .eng header for different motors
- Geometry based drag build-up
- Parachute Deployment
- RK4 Integration Method (Instead of Euler; larger stable timesteps)
- Monte Carlo Simulation




