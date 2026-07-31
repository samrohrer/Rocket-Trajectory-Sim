from models import Rocket, Environment, FlightState
from config import DRY_MASS, PROPELLANT_MASS, BURN_TIME, DRAG_COEFFICIENT, CROSS_SEC_AREA, SEA_LEVEL_DENSITY, ATMOSPHERIC_SCALE_HEIGHT, STANDARD_GRAVITY, VELOCITY, ALTITUDE, TIME, DT
from plotting import plot_flight_summary
from simulation import simulate_flight
import numpy as np

def main() -> None:
    """Runs the flight simulation for the configured rocket, then plots the flight parameters and prints the apogee"""
    rocket = Rocket(dry_mass=DRY_MASS, propellant_mass=PROPELLANT_MASS, burn_time=BURN_TIME, drag_coefficient=DRAG_COEFFICIENT, cross_sec_area=CROSS_SEC_AREA)
    environment = Environment(density_sea_level=SEA_LEVEL_DENSITY, atmospheric_scale_height=ATMOSPHERIC_SCALE_HEIGHT, g=STANDARD_GRAVITY)
    state = FlightState(velocity=VELOCITY, altitude=ALTITUDE, time=TIME)
    simulate_flight(rocket, environment, state, dt=DT)
    plot_flight_summary(state, rocket)
    print(np.max(state.altitude_list))
    print(np.max(state.velocity_list))

if __name__ == "__main__":
    main()