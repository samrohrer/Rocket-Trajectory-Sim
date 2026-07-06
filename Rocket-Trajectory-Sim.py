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
#Lists of Altitudes and Times for every step
altitude_list = []
time_list = []

def calculate_thrust(time, burn_time):
    if time < burn_time:
        thrust = 2500
    else:
        thrust = 0
    return thrust

def calculate_density(density_sea_level, altitude, atmosphere_scale_height):
    density = density_sea_level * np.exp(-altitude / atmospheric_scale_height)
    return density

def calculate_drag(drag_coefficient, density, velocity, cross_sec_area):
    drag = drag_coefficient * density * velocity ** 2 / 2 * cross_sec_area
    if velocity > 0:
        drag = -drag
    else:
        drag = +drag
    return drag

def calculate_acceleration(thrust, drag, mass, g):
    acceleration = (thrust + drag + mass * g) / mass
    return acceleration

def update_velocity(velocity, acceleration, dt):
    new_velocity = velocity + acceleration * dt
    return new_velocity

def update_altitude(altitude, new_velocity, dt):
    new_altitude = altitude + new_velocity * dt
    return new_altitude

#While loop calculating altitude
while altitude >= 0:
    thrust = calculate_thrust(time, burn_time)
    density = calculate_density(density_sea_level, altitude, atmospheric_scale_height)
    drag = calculate_drag(drag_coefficient, density, velocity, cross_sec_area)
    acceleration = calculate_acceleration(thrust, drag, mass, g)
    velocity = update_velocity(velocity, acceleration, dt)
    altitude = update_altitude(altitude, velocity, dt)

    time = time + dt
    print(altitude)
    altitude_list.append(altitude)
    time_list.append(time)

#Plotting the Altitudes and Time
plt.plot(time_list, altitude_list)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.show()



