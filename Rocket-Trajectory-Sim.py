import numpy as np
import matplotlib.pyplot as plt

#Initial Constants
velocity = 20 #m/s
altitude = 0 #m
time = 0 #s
mass = 34 #kg
dt = 0.1 #s
g = -9.81 #m/s/s
burn_time = 3.9 #s
drag_coefficient = 0.5  #Cd
cross_sec_area = 0.0193  #m^2
density_sea_level = 1.225  #kg/m^3
atmospheric_scale_height = 8500 #m

def calculate_thrust(time, burn_time):
    """Calculates the thrust of the flight simulation."""
    if time < burn_time:
        thrust = 2500
    else:
        thrust = 0
    return thrust

def calculate_density(density_sea_level, altitude, atmospheric_scale_height):
    """Calculates the density of the flight simulation."""
    density = density_sea_level * np.exp(-altitude / atmospheric_scale_height)
    return density

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

def update_velocity(velocity, acceleration, dt):
    """Updates the velocity of the flight simulation."""
    new_velocity = velocity + acceleration * dt
    return new_velocity

def update_altitude(altitude, new_velocity, dt):
    """Updates the altitude of the flight simulation."""
    new_altitude = altitude + new_velocity * dt
    return new_altitude

def simulate_flight(velocity, altitude, time, mass, dt, burn_time, g, drag_coefficient, cross_sec_area, density_sea_level, atmospheric_scale_height):
    """Runs the flight simulation loop and returns (altitude_list, time_list)."""
    altitude_list = []
    time_list = []
    while altitude >= 0:
        thrust = calculate_thrust(time, burn_time)
        density = calculate_density(density_sea_level, altitude, atmospheric_scale_height)
        drag = calculate_drag(drag_coefficient, density, velocity, cross_sec_area)
        acceleration = calculate_acceleration(thrust, drag, mass, g)
        velocity = update_velocity(velocity, acceleration, dt)
        altitude = update_altitude(altitude, velocity, dt)
        time = time + dt
        altitude_list.append(altitude)
        time_list.append(time)
    return time_list, altitude_list

def plot_results(time_list, altitude_list):
    """Plots the results of the flight simulation."""
    plt.plot(time_list, altitude_list)
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.show()

def main():
    """Runs the flight simulation loop."""
    time_list, altitude_list = simulate_flight(velocity, altitude, time, mass, dt, burn_time, g, drag_coefficient, cross_sec_area,
                    density_sea_level, atmospheric_scale_height)
    plot_results(time_list, altitude_list)

if __name__ == "__main__":
    main()



