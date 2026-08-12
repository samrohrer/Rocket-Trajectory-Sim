import numpy as np
from dataclasses import dataclass

@dataclass
class Motor:
    """Records the motor attributes associated with the rocket's motor
    Holds the propellant mass, motor mass, thrust curve data, and calculates the total impulse using trapezoidal integration of the thrust curve
    motor_mass is total mass of the motor including propellant"""
    propellant_mass: float
    motor_mass: float
    times: np.ndarray
    thrusts: np.ndarray

    def __post_init__(self) -> None:
        self.impulse_total: float = np.trapezoid(self.thrusts, self.times)

def load_motor(filepath: str) -> Motor:
    """Reads motor format from .eng file; lines starting with ";" are comments and ignored, first non-comment line is a header, subsequent lines are time and thrust values
    [4] and [5] are propellant mass and motor mass, respectively, which are read from the first non-comment line"""
    propellant_mass = None
    motor_mass = None
    times = []
    thrusts = []

    with open(filepath) as f:
        for line in f:
            if line.startswith(";"):
                continue
            fields = line.split()
            if propellant_mass is None:
                propellant_mass, motor_mass = float(fields[4]), float(fields[5])
            else:
                times.append(float(fields[0]))
                thrusts.append(float(fields[1]))

    return Motor(
        propellant_mass=propellant_mass,
        motor_mass=motor_mass,
        times=np.array(times),
        thrusts=np.array(thrusts),
    )

@dataclass
class CdCurve:
    drag_coefficient: np.ndarray
    mach_numbers: np.ndarray

def load_cd_curve(filepath: str) -> CdCurve:
    drag_coefficient = []
    mach_numbers = []

    with open(filepath) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.split(",")
            drag_coefficient.append(float(fields[0]))
            mach_numbers.append(float(fields[1]))

    drag_coefficient = np.array(drag_coefficient)
    mach_numbers = np.array(mach_numbers)
    sort_order = np.argsort(mach_numbers)
    drag_coefficient = drag_coefficient[sort_order]
    mach_numbers = mach_numbers[sort_order]

    mach_numbers, keep_indices = np.unique(mach_numbers, return_index=True)
    drag_coefficient = drag_coefficient[keep_indices]

    return CdCurve(
        drag_coefficient=drag_coefficient,
        mach_numbers=mach_numbers
    )

class Rocket:
    """Records the rocket attributes associated with the rocket body and motor
    Holds current values such as mass and historical values that are stored in lists"""
    def __init__(self, drag_coefficient: float, cross_sec_area: float, dry_mass: float, motor: Motor) -> None:
        self.drag_coefficient: float = drag_coefficient
        self.cross_sec_area: float = cross_sec_area
        self.dry_mass: float = dry_mass
        self.propellant_mass: float = motor.propellant_mass
        self.thrust_times: np.ndarray = motor.times
        self.thrust_values: np.ndarray = motor.thrusts
        self.impulse_total: float = motor.impulse_total

    def get_thrust_at(self, t: float) -> float:
        """Determines the thrust value of the simulation at a given time using np.interp function, interpolating within the motor's thrust curve data."""
        return np.interp(t, self.thrust_times, self.thrust_values, right=0)

    def calculate_mass(self, impulse: float) -> float:
        """Calculates the variable mass of the rocket during flight simulation using a mass depletion model: Mass depletes proportionally to consumed impulse
        Propellant mass is added to the total mass of the rocket, using a shrinking value until the impulse equation cancels out and reaches the total impulse"""
        mass = self.dry_mass + self.propellant_mass * np.clip((1 - impulse / self.impulse_total), 0, 1)
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