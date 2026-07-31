from models import Rocket, Environment, FlightState

def simulate_flight(rocket: Rocket, environment: Environment, state: FlightState, dt: float) -> None:
    """Runs the flight simulation loop until the rocket lands (altitude reaches 0). Each timestep's values are appended to their respective lists before velocity and altitude are updated, so every recorded value reflects the same consistent moment in flight"""
    has_launched = False

    while not has_launched or state.altitude >= 0:
        if not has_launched and state.altitude <= 0:
            state.velocity = 0
            state.altitude = 0
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
        if state.altitude > 0:
            has_launched = True
        state.time = state.time + dt