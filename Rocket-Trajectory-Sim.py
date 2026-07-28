import numpy as np
import matplotlib.pyplot as plt

# Physical/Environmental Constants
STANDARD_GRAVITY = -9.81
SEA_LEVEL_DENSITY = 1.225
ATMOSPHERIC_SCALE_HEIGHT = 8500

# Rocket Specifications (Currently Spartacus MKIII)
DRY_MASS = 22
PROPELLANT_MASS = 4.717361
BURN_TIME = 3.9
DRAG_COEFFICIENT = 0.447
CROSS_SEC_AREA = 0.01824
CSV_FILE_NAME = 'data/AeroTech_M2500T.csv'
CSV_HEADER_ROWS = 5

# Simulation Setup/Initial Conditions
VELOCITY = 30
ALTITUDE = 0
TIME = 0
DT = 0.01


class Rocket:
    """Records the rocket attributes associated with the rocket body and motor
    Thrust curve is loaded from a CSV file"""
    def __init__(self, burn_time: float, drag_coefficient: float, cross_sec_area: float, dry_mass: float, propellant_mass: float) -> None:
        self.burn_time: float = burn_time
        self.drag_coefficient: float = drag_coefficient
        self.cross_sec_area: float = cross_sec_area
        self.dry_mass: float = dry_mass
        self.propellant_mass: float = propellant_mass
        data = np.genfromtxt(CSV_FILE_NAME, delimiter=',', skip_header=CSV_HEADER_ROWS)
        self.thrust_times: np.ndarray = data[:, 0]
        self.thrust_values: np.ndarray = data[:, 1]
        self.impulse_total: float = np.trapezoid(self.thrust_values, self.thrust_times)

    def get_thrust_at(self, t: float) -> float:
        """Determines the thrust value of the simulation at a given time using np.interp function, interpolating within the motor's thrust curve data."""
        return np.interp(t, self.thrust_times, self.thrust_values, right=0)

    def calculate_mass(self, time: float, impulse: float) -> float:
        """Calculates the variable mass of the rocket during flight simulation using a mass depletion model: Mass depletes proportionally to consumed impulse
        Propellant mass is added to the total mass of the rocket, using a shrinking value, until the time of the simulation exceeds the motor's burn_time."""
        if time < self.burn_time:
            mass = self.dry_mass + self.propellant_mass * (1 - impulse / self.impulse_total)
        else:
            mass = self.dry_mass
        return mass

    def calculate_drag(self, density: float, velocity: float) -> float:
        """Calculates aerodynamic drag force using drag = Cd * density * velocity^2 / 2 * cross_sec_area
        Drag opposes motion, so the sign is flipped opposite to the current direction of velocity"""
        drag: float = self.drag_coefficient * density * velocity ** 2 / 2 * self.cross_sec_area
        if velocity > 0:
            drag = -drag
        else:
            drag = +drag
        return drag

class Environment:
    """Records the atmospheric and gravitational fields that the rocket experiences during flight"""
    def __init__(self, density_sea_level: float, atmospheric_scale_height: float, g: float) -> None:
        self.density_sea_level: float = density_sea_level
        self.atmospheric_scale_height: float = atmospheric_scale_height
        self.g: float = g

    def calculate_density(self, altitude: float) -> float:
        """Calculates the variable density using an Isothermal Barometric Formula: density_sea_level * e^(-altitude/atmospheric_scale_height)"""
        density: float = self.density_sea_level * np.exp(-altitude / self.atmospheric_scale_height)
        return density

    def calculate_acceleration(self, thrust: float, drag: float, mass: float) -> float:
        """Calculates the acceleration of the flight simulation deriving Newton's Second Law formula (F = ma) to get acceleration: a = (thrust + drag + mass * g) / mass
        Drag sign is already accounted for in calculate_drag"""
        acceleration: float = (thrust + drag + mass * self.g) / mass
        return acceleration

class FlightState:
    """Records the flight values associated with the rocket's flight simulation state
    Holds current values such as velocity and historical values that are stored in lists"""
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
        """Velocity is updated at the end of all the calculations, in accordance with the time step (dt), so the next round of calculations uses an updated velocity
        Updates velocity using forward Euler integration: velocity = velocity + acceleration * dt"""
        self.velocity = self.velocity + acceleration * dt

    def update_altitude(self, dt: float) -> None:
        """Altitude is updated at the end of all the calculations, in accordance with the time step (dt), so the next round of calculations uses an updated altitude
        Updates altitude using forward Euler integration: altitude = altitude + velocity * dt"""
        self.altitude = self.altitude + self.velocity * dt

def simulate_flight(rocket: Rocket, environment: Environment, state: FlightState, dt: float) -> None:
    """Runs the flight simulation loop until the rocket lands (altitude reaches 0). Each timestep's values are appended to their respective lists before velocity and altitude are updated, so every recorded value reflects the same consistent moment in flight"""
    while state.altitude >= 0:
        state.thrust = rocket.get_thrust_at(state.time)
        state.density = environment.calculate_density(state.altitude)
        state.impulse += state.thrust * dt
        state.mass = rocket.calculate_mass(state.time, state.impulse)
        state.drag = rocket.calculate_drag(state.density, state.velocity)
        state.acceleration = environment.calculate_acceleration(state.thrust, state.drag, state.mass)
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

def main() -> None:
    """Runs the flight simulation for the configured rocket, then plots the flight parameters and prints the apogee"""
    rocket = Rocket(dry_mass=DRY_MASS, propellant_mass=PROPELLANT_MASS, burn_time=BURN_TIME, drag_coefficient=DRAG_COEFFICIENT, cross_sec_area=CROSS_SEC_AREA)
    environment = Environment(density_sea_level=SEA_LEVEL_DENSITY, atmospheric_scale_height=ATMOSPHERIC_SCALE_HEIGHT, g=STANDARD_GRAVITY)
    state = FlightState(velocity=VELOCITY, altitude=ALTITUDE, time=TIME)
    simulate_flight(rocket, environment, state, dt=DT)
    plot_flight_summary(state, rocket)
    print(np.max(state.altitude_list))

if __name__ == "__main__":
    main()