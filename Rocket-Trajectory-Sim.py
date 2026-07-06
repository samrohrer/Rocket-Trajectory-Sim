import numpy as np
import matplotlib.pyplot as plt

#Initial Constants
velocity = 20
altitude = 0
time = 0
mass = 34
dt = 0.1
g = -9.81
drag_coefficient = 0.5  # Cd
cross_sec_area = 0.0193  # m^2
density_rho = 1.225  # kg/m^3
#Lists of Altitudes and Times for every step
altitude_list = []
time_list = []

#While loop calculating altitude
while altitude >= 0:
    burn_time = 3.9
    #If statement determining whether thrust is on or off
    if time < burn_time:
        thrust = 2500
    else:
        thrust = 0
    #Drag equation added as a force in acceleration
    drag_equation = drag_coefficient * density_rho * velocity ** 2 / 2 * cross_sec_area
    if velocity > 0:
        drag_equation = -drag_equation
    else:
        drag_equation = +drag_equation
    acceleration = (thrust + drag_equation + mass*g)/mass
    new_velocity = velocity + acceleration * dt
    new_altitude = altitude + new_velocity * dt
    time = time + dt
    velocity = new_velocity
    altitude = new_altitude
    altitude_list.append(altitude)
    time_list.append(time)

#Plotting the Altitudes and Time
plt.plot(time_list, altitude_list)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.show()