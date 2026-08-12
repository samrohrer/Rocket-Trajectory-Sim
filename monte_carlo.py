import numpy as np
from models import Motor, CdCurve, Rocket, Environment, FlightState
from config import DRY_MASS_STD, MOTOR_SCALE_STD, DRAG_COEFFICIENT_STD, SEA_LEVEL_DENSITY_STD, ATMOSPHERIC_SCALE_HEIGHT, STANDARD_GRAVITY, N_TRIALS, VELOCITY, ALTITUDE, TIME, DT
from simulation import simulate_flight

rng = np.random.default_rng()

def generate_random_trial(motor, dry_mass, cd_curve, cross_sec_area, sea_level_density):
    dry_mass_sample = rng.normal(loc=dry_mass, scale=DRY_MASS_STD*dry_mass)
    k_sample = rng.normal(loc=1.0, scale=MOTOR_SCALE_STD)
    cd_scale_factor = rng.normal(loc=1.0, scale=DRAG_COEFFICIENT_STD)
    sea_level_density_sample = rng.normal(loc=sea_level_density, scale=SEA_LEVEL_DENSITY_STD*sea_level_density)

    sampled_motor = Motor(
        propellant_mass=motor.propellant_mass,
        motor_mass=motor.motor_mass,
        times=motor.times * k_sample,
        thrusts=motor.thrusts * (1 / k_sample),
    )

    sampled_cd_curve = CdCurve(
        drag_coefficient=cd_curve.drag_coefficient * cd_scale_factor,
        mach_numbers=cd_curve.mach_numbers
    )

    sampled_rocket = Rocket(
        dry_mass=dry_mass_sample,
        cd_curve=sampled_cd_curve,
        cross_sec_area=cross_sec_area,
        motor=sampled_motor
    )

    sampled_environment = Environment(
        density_sea_level=sea_level_density_sample,
        atmospheric_scale_height=ATMOSPHERIC_SCALE_HEIGHT,
        g=STANDARD_GRAVITY
    )

    return sampled_rocket, sampled_environment

def run_monte_carlo(motor, dry_mass, cd_curve, cross_sec_area, sea_level_density, N_TRIALS):
    apogee_list = []
    max_velocity_list = []
    for i in range(N_TRIALS):
        sampled_rocket, sampled_environment = generate_random_trial(motor, dry_mass, cd_curve, cross_sec_area, sea_level_density)
        state = FlightState(velocity=VELOCITY, altitude=ALTITUDE, time=TIME)
        simulate_flight(sampled_rocket, sampled_environment, state, dt=DT)
        apogee_list.append(np.max(state.altitude_list))
        max_velocity_list.append(np.max(state.velocity_list))
    return apogee_list, max_velocity_list
