import numpy as np
import matplotlib.pyplot as plt

class Rocket:
    def __init__(self, burn_time, drag_coefficient, cross_sec_area, dry_mass, propellant_mass):
        self.burn_time = burn_time
        self.drag_coefficient = drag_coefficient
        self.cross_sec_area = cross_sec_area
        self.dry_mass = dry_mass
        self.propellant_mass = propellant_mass
        data = np.genfromtxt('data/AeroTech_M2500T.csv', delimiter=',', skip_header=5)
        self.thrust_times = data[:, 0]
        self.thrust_values = data[:, 1]

    def get_thrust_at(self, t):
        return np.interp(t, self.thrust_times, self.thrust_values, right=0)


class Environment:
    def __init__(self, density_sea_level, atmospheric_scale_height, g):
        self.density_sea_level = density_sea_level
        self.atmospheric_scale_height = atmospheric_scale_height
        self.g = g

class FlightState:
    def __init__(self, velocity, altitude, time):
        self.velocity = velocity
        self.altitude = altitude
        self.time = time
        self.mass = 0
        self.acceleration = 0
        self.thrust = 0
        self.drag = 0
        self.density = 0
        self.time_list = []
        self.altitude_list = []

    def update_velocity(self, acceleration, dt):
        self.velocity = self.velocity + acceleration * dt

    def update_altitude(self, dt):
        self.altitude = self.altitude + self.velocity * dt

def calculate_thrust(time, rocket):
    """Calculates the thrust of the flight simulation."""
    thrust = rocket.get_thrust_at(time)
    return thrust

def calculate_density(density_sea_level, altitude, atmospheric_scale_height):
    """Calculates the density of the flight simulation."""
    density = density_sea_level * np.exp(-altitude / atmospheric_scale_height)
    return density

def calculate_mass(dry_mass, propellant_mass, burn_time, time):
    """Calculates the current mass of the rocket."""
    if time < burn_time:
        mass = dry_mass + propellant_mass * (1-time/burn_time)
    else:
        mass = dry_mass
    return mass

def calculate_drag(drag_coefficient, density, velocity, cross_sec_area):
    """Calculates the drag of the flight simulation."""
    drag = drag_coefficient * density * velocity ** 2 / 2 * cross_sec_area
    if velocity > 0:
        drag = -drag
    else:
        drag = +drag
    return drag

def calculate_acceleration(thrust, drag, mass, g):
    """Calculates the acceleration of the flight simulation."""
    acceleration = (thrust + drag + mass * g) / mass
    return acceleration

def simulate_flight(rocket, environment, state, dt):
    while state.altitude >= 0:
        state.thrust = calculate_thrust(state.time, rocket)
        state.density = calculate_density(environment.density_sea_level, state.altitude, environment.atmospheric_scale_height)
        state.mass = calculate_mass(rocket.dry_mass, rocket.propellant_mass, rocket.burn_time, state.time)
        state.drag = calculate_drag(rocket.drag_coefficient, state.density, state.velocity, rocket.cross_sec_area)
        state.acceleration = calculate_acceleration(state.thrust, state.drag, state.mass, environment.g)
        state.update_velocity(state.acceleration, dt)
        state.update_altitude(dt)
        state.time = state.time + dt
        state.altitude_list.append(state.altitude)
        state.time_list.append(state.time)

def plot_results(time_list, altitude_list):
    """Plots the results of the flight simulation."""
    plt.plot(time_list, altitude_list)
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.show()

def main():
    """Runs the flight simulation loop."""
    rocket = Rocket(dry_mass=29.9, propellant_mass=4.531, burn_time=3.9, drag_coefficient=0.5, cross_sec_area=0.0193)
    environment = Environment(density_sea_level=1.225, atmospheric_scale_height=8500, g=-9.81)
    state = FlightState(velocity=20, altitude=0, time=0)
    dt = 0.1
    simulate_flight(rocket, environment, state, dt)
    plot_results(state.time_list, state.altitude_list)

if __name__ == "__main__":
    main()





