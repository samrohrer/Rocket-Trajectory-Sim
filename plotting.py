from models import FlightState, Rocket
import matplotlib.pyplot as plt
import numpy as np

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