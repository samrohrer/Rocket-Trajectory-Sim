from models import Rocket, Environment, FlightState, load_motor
from config import DRY_MASS, DRAG_COEFFICIENT, CROSS_SEC_AREA, SEA_LEVEL_DENSITY, ATMOSPHERIC_SCALE_HEIGHT, STANDARD_GRAVITY, VELOCITY, ALTITUDE, TIME, DT
from plotting import plot_flight_summary
from simulation import simulate_flight
import numpy as np

def main() -> None:
    """Runs the flight simulation for the configured rocket, then plots the flight parameters and prints the apogee"""
    motor = load_motor("data/AeroTech_M2500T.eng")
    rocket = Rocket(dry_mass=DRY_MASS, drag_coefficient=DRAG_COEFFICIENT, cross_sec_area=CROSS_SEC_AREA, motor=motor)
    environment = Environment(density_sea_level=SEA_LEVEL_DENSITY, atmospheric_scale_height=ATMOSPHERIC_SCALE_HEIGHT, g=STANDARD_GRAVITY)
    state = FlightState(velocity=VELOCITY, altitude=ALTITUDE, time=TIME)
    simulate_flight(rocket, environment, state, dt=DT)
    plot_flight_summary(state, rocket)
    print(f"Apogee: {np.max(state.altitude_list):.1f} m")
    print(f"Max Velocity: {np.max(state.velocity_list):.1f} m/s")
    print(f"Total impulse: {motor.impulse_total:.1f} N·s")

if __name__ == "__main__":
    main()