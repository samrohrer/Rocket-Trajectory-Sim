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

#While loop calculating altitude
while altitude >= 0:
    #If statement determining whether thrust is on or off
    if time < burn_time:
        thrust = 2500
    else:
        thrust = 0

    #Exponential Atmospheric Model based on Isothermal Atmosphere
    density_current = density_sea_level * np.exp(-altitude/atmospheric_scale_height)

    #Drag equation added as a force in acceleration
    drag_equation = drag_coefficient * density_current * velocity ** 2 / 2 * cross_sec_area
    #If statement deciding which direction drag force acts
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
