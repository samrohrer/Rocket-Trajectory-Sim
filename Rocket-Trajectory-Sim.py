import numpy as np
import matplotlib.pyplot as plt

class Rocket:
    def __init__(self, burn_time: float, drag_coefficient: float, cross_sec_area: float, dry_mass: float, propellant_mass: float) -> None:
        self.burn_time: float = burn_time
        self.drag_coefficient: float = drag_coefficient
        self.cross_sec_area: float = cross_sec_area
        self.dry_mass: float = dry_mass
        self.propellant_mass: float = propellant_mass
        data = np.genfromtxt('data/AeroTech_M2500T.csv', delimiter=',', skip_header=5)
        self.thrust_times: np.ndarray = data[:, 0]
        self.thrust_values: np.ndarray = data[:, 1]
        self.impulse_total: float = np.trapezoid(self.thrust_values, self.thrust_times)

    def get_thrust_at(self, t: float) -> float:
        return np.interp(t, self.thrust_times, self.thrust_values, right=0)


class Environment:
    def __init__(self, density_sea_level: float, atmospheric_scale_height: float, g: float) -> None:
        self.density_sea_level: float = density_sea_level
        self.atmospheric_scale_height: float = atmospheric_scale_height
        self.g: float = g

class FlightState:
    def __init__(self, velocity: float, altitude: float, time: float) -> None:
        self.velocity: float = velocity
        self.altitude: float = altitude
        self.time: float = time
        self.mass: float = 0
        self.acceleration: float = 0
        self.thrust: float = 0
        self.drag: float = 0
        self.density: float = 0
        self.impulse: float = 0
        self.time_list: list[float] = []
        self.altitude_list: list[float] = []
        self.velocity_list: list[float] = []
        self.acceleration_list: list[float] = []
        self.thrust_list: list[float] = []
        self.drag_list: list[float] = []
        self.mass_list: list[float] = []

    def update_velocity(self, acceleration: float, dt: float) -> None:
        self.velocity = self.velocity + acceleration * dt

    def update_altitude(self, dt: float) -> None:
        self.altitude = self.altitude + self.velocity * dt

def calculate_thrust(time: float, rocket: Rocket) -> float:
    """Calculates the thrust of the flight simulation."""
    thrust: float = rocket.get_thrust_at(time)
    return thrust

def calculate_density(density_sea_level: float, altitude: float, atmospheric_scale_height: float) -> float:
    """Calculates the density of the flight simulation."""
    density: float = density_sea_level * np.exp(-altitude / atmospheric_scale_height)
    return density

def calculate_mass(dry_mass: float, propellant_mass: float, burn_time: float, time: float, impulse: float, impulse_total: float) -> float:
    """Calculates the current mass of the rocket."""
    if time < burn_time:
        mass = dry_mass + propellant_mass * (1-impulse/impulse_total)
    else:
        mass = dry_mass
    return mass

def calculate_drag(drag_coefficient: float, density: float, velocity: float, cross_sec_area: float) -> float:
    """Calculates the drag of the flight simulation."""
    drag: float = drag_coefficient * density * velocity ** 2 / 2 * cross_sec_area
    if velocity > 0:
        drag = -drag
    else:
        drag = +drag
    return drag

def calculate_acceleration(thrust: float, drag: float, mass: float, g: float) -> float:
    """Calculates the acceleration of the flight simulation."""
    acceleration: float = (thrust + drag + mass * g) / mass
    return acceleration

def simulate_flight(rocket: Rocket, environment: Environment, state: FlightState, dt: float) -> None:
    while state.altitude >= 0:
        state.thrust = calculate_thrust(state.time, rocket)
        state.density = calculate_density(environment.density_sea_level, state.altitude, environment.atmospheric_scale_height)
        state.impulse += state.thrust * dt
        state.mass = calculate_mass(rocket.dry_mass, rocket.propellant_mass, rocket.burn_time, state.time, state.impulse, rocket.impulse_total)
        state.drag = calculate_drag(rocket.drag_coefficient, state.density, state.velocity, rocket.cross_sec_area)
        state.acceleration = calculate_acceleration(state.thrust, state.drag, state.mass, environment.g)
        state.altitude_list.append(state.altitude)
        state.time_list.append(state.time)
        state.velocity_list.append(state.velocity)
        state.acceleration_list.append(state.acceleration)
        state.thrust_list.append(state.thrust)
        state.drag_list.append(state.drag)
        state.mass_list.append(state.mass)
        state.update_velocity(state.acceleration, dt)
        state.update_altitude(dt)
        state.time = state.time + dt

def plot_flight_summary(state: FlightState, rocket: Rocket) -> None:
    """Plots flight parameters vs time in a multi-panel figure."""
    apogee_index = np.argmax(state.altitude_list)
    apogee_time = state.time_list[apogee_index]
    burnout_time = rocket.thrust_times[-1]

    fig, axs = plt.subplots(nrows=3, ncols=2, sharex=True, figsize=(12, 10))

    axs[0, 0].plot(state.time_list, state.thrust_list, label="Thrust")
    axs[0, 0].plot(state.time_list, state.drag_list, label="Drag")
    axs[0, 0].set_ylabel("Force (N)")
    axs[0, 0].set_title("Thrust and Drag vs Time")

    axs[0, 1].plot(state.time_list, state.mass_list)
    axs[0, 1].set_ylabel("Mass (kg)")
    axs[0, 1].set_title("Mass vs Time")

    axs[1, 0].plot(state.time_list, state.acceleration_list)
    axs[1, 0].set_ylabel("Acceleration (m/s^2)")
    axs[1, 0].set_title("Acceleration vs Time")

    axs[1, 1].plot(state.time_list, state.velocity_list)
    axs[1, 1].set_ylabel("Velocity (m/s)")
    axs[1, 1].set_title("Velocity vs Time")

    axs[2, 0].plot(state.time_list, state.altitude_list)
    axs[2, 0].set_ylabel("Altitude (m)")
    axs[2, 0].set_xlabel("Time (s)")

    data_axes = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1], axs[2, 0]]

    for ax in data_axes:
        ax.axvline(x=burnout_time, color='gray', linestyle='--', label='Burnout')
        ax.axvline(x=apogee_time, color='red', linestyle='--', label='Apogee')
        ax.grid(True)

    axs[0, 0].legend()
    axs[2, 1].axis("off")
    plt.tight_layout()
    plt.show()

def main():
    """Runs the flight simulation loop."""
    rocket = Rocket(dry_mass=22, propellant_mass=4.717361, burn_time=3.9, drag_coefficient=0.447, cross_sec_area=0.01824)
    environment = Environment(density_sea_level=1.225, atmospheric_scale_height=8500, g=-9.81)
    state = FlightState(velocity=30, altitude=0, time=0)
    dt = 0.01
    simulate_flight(rocket, environment, state, dt)
    plot_flight_summary(state, rocket)
    print(np.max(state.altitude_list))

if __name__ == "__main__":
    main()



T

