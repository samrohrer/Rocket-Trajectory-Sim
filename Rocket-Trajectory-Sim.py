import numpy as np
import matplotlib.pyplot as plt

#Initial Constants
velocity = 20
altitude = 0
time = 0
mass = 5
dt = 0.1
g = -9.81
#Lists of Altitudes and Times for every step
altitude_list = []
time_list = []

#While Loop for velocity and altitude
while altitude >= 0:
    acceleration = g
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

