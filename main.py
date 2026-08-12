from models import Rocket, Environment, FlightState, load_motor, load_cd_curve
from config import DRY_MASS, CROSS_SEC_AREA, SEA_LEVEL_DENSITY, ATMOSPHERIC_SCALE_HEIGHT, STANDARD_GRAVITY, VELOCITY, ALTITUDE, TIME, DT, N_TRIALS
from plotting import plot_flight_summary, plot_monte_carlo_results, plot_cd_curve
from simulation import simulate_flight
from monte_carlo import run_monte_carlo
import numpy as np
import matplotlib.pyplot as plt

def main() -> None:
    """Runs the flight simulation for the configured rocket, then plots the flight parameters and prints the apogee"""
    motor = load_motor("data/AeroTech_M2500T.eng")
    cd_curve = load_cd_curve("data/mkiii_cd_mach.csv")
    rocket = Rocket(dry_mass=DRY_MASS, cross_sec_area=CROSS_SEC_AREA, motor=motor, cd_curve=cd_curve)
    environment = Environment(density_sea_level=SEA_LEVEL_DENSITY, atmospheric_scale_height=ATMOSPHERIC_SCALE_HEIGHT, g=STANDARD_GRAVITY)
    state = FlightState(velocity=VELOCITY, altitude=ALTITUDE, time=TIME)
    simulate_flight(rocket, environment, state, dt=DT)
    plot_flight_summary(state, rocket)
    apogee_list, max_velocity_list = run_monte_carlo(motor, DRY_MASS, cd_curve, CROSS_SEC_AREA, SEA_LEVEL_DENSITY, N_TRIALS)
    plot_monte_carlo_results(apogee_list, max_velocity_list)
    plot_cd_curve(rocket, state)
    print(f"Apogee: {np.max(state.altitude_list):.1f} m")
    print(f"Max Velocity: {np.max(state.velocity_list):.1f} m/s")
    print(f"Total impulse: {motor.impulse_total:.1f} N·s")
    plt.show()

if __name__ == "__main__":
    main()