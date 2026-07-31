from dataclasses import dataclass

@dataclass
class Motor:
    propellant_mass: float
    motor_mass: float
    times: list[float]
    thrusts: list[float]

def load_motor(filepath: str) -> Motor:
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
        times=times,
        thrusts=thrusts,
    )

motor = load_motor("data/AeroTech_M2500T.eng")
print(motor.propellant_mass, motor.motor_mass, len(motor.times), len(motor.thrusts))