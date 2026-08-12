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
    axs[0, 0].set_xlabel("Time (s)")
    axs[0, 0].set_title("Thrust and Drag vs Time")

    axs[0, 1].plot(state.time_list, state.mass_list)
    axs[0, 1].set_ylabel("Mass (kg)")
    axs[0, 1].set_xlabel("Time (s)")
    axs[0, 1].set_title("Mass vs Time")

    axs[1, 0].plot(state.time_list, state.acceleration_list)
    axs[1, 0].set_ylabel("Acceleration (m/s^2)")
    axs[1, 0].set_xlabel("Time (s)")
    axs[1, 0].set_title("Acceleration vs Time")

    axs[1, 1].plot(state.time_list, state.velocity_list)
    axs[1, 1].set_ylabel("Velocity (m/s)")
    axs[1, 1].set_xlabel("Time (s)")
    axs[1, 1].set_title("Velocity vs Time")

    axs[2, 0].plot(state.time_list, state.altitude_list)
    axs[2, 0].set_ylabel("Altitude (m)")
    axs[2, 0].set_xlabel("Time (s)")
    axs[2, 0].set_title("Altitude vs Time")

    data_axes = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1], axs[2, 0]]

    for ax in data_axes:
        ax.axvline(x=burnout_time, color='gray', linestyle='--', label='Burnout')
        ax.axvline(x=apogee_time, color='red', linestyle='--', label='Apogee')
        ax.grid(True)

    axs[0, 0].legend()
    axs[2, 1].axis("off")
    plt.tight_layout()
    
def plot_monte_carlo_results(apogee_list: list[float], max_velocity_list: list[float]) -> None:
    """Plots histograms of apogee and max velocity results from Monte Carlo simulation."""
    apogee_mean = np.mean(apogee_list)
    apogee_std = np.std(apogee_list)
    max_velocity_mean = np.mean(max_velocity_list)
    max_velocity_std = np.std(max_velocity_list)

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    axs[0].hist(apogee_list, bins=20, color='lightblue', alpha=0.7, rwidth=0.9)
    axs[0].set_title("Apogee Distribution")
    axs[0].set_xlabel("Apogee (m)")
    axs[0].set_ylabel("Number of Occurrences")
    axs[0].axvline(x=apogee_mean, color='red', linestyle='--', label=f'Mean: {apogee_mean:.2f} m')
    axs[0].axvline(x=apogee_mean + apogee_std, color='green', linestyle='--', label=f'+1 Std Dev: {apogee_mean + apogee_std:.2f} m')
    axs[0].axvline(x=apogee_mean - apogee_std, color='green', linestyle='--', label=f'-1 Std Dev: {apogee_mean - apogee_std:.2f} m')
    axs[0].legend()

    axs[1].hist(max_velocity_list, bins=20, color='lightblue', alpha=0.7, rwidth=0.9)
    axs[1].set_title("Max Velocity Distribution")
    axs[1].set_xlabel("Max Velocity (m/s)")
    axs[1].set_ylabel("Number of Occurrences")
    axs[1].axvline(x=max_velocity_mean, color='red', linestyle='--', label=f'Mean: {max_velocity_mean:.2f} m/s')
    axs[1].axvline(x=max_velocity_mean + max_velocity_std, color='green', linestyle='--', label=f'+1 Std Dev: {max_velocity_mean + max_velocity_std:.2f} m/s')
    axs[1].axvline(x=max_velocity_mean - max_velocity_std, color='green', linestyle='--', label=f'-1 Std Dev: {max_velocity_mean - max_velocity_std:.2f} m/s')
    axs[1].legend()

    plt.tight_layout()

def plot_cd_curve(rocket: Rocket, state: FlightState) -> None:
    """Plots the drag coefficient curve of the rocket and overlays the flight data points."""
    flight_cd = []
    for mach in state.mach_list:
        flight_cd.append(rocket.get_drag_coefficient(mach))

    plt.figure(figsize=(8, 6))
    plt.plot(rocket.mach_numbers, rocket.drag_coefficients, label='Interoplated Cd Curve', color='blue')
    plt.scatter(state.mach_list, flight_cd, color='orange', label='Flight Data Points', s=5, alpha=0.5)
    plt.axvline(x=max(state.mach_list), color='red', linestyle='--', label=f'Peak Mach: {max(state.mach_list):.2f}')
    plt.xlabel('Mach Number')
    plt.ylabel('Drag Coefficient (Cd)')
    plt.title('Drag Coefficient vs Mach Number')
    plt.legend()
    plt.grid(True)