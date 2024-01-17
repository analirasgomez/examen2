import json
import math
import PySimpleGUI as sg

# Definir el JSON directamente en el código
with open ("examen.json", "r") as j:
    json_data = json.load(j)

json_data = """
{
    "launches": [
        {"index": 1, "velocity": 20.0, "angle": 30.0},
        {"index": 2, "velocity": 15.0, "angle": 45.0},
        {"index": 3, "velocity": 25.0, "angle": 60.0},
        {"index": 4. "velocity": 28.0, "angle": 40.0}
    ]
}
"""

def calculate_position(velocity, angle, time):
    # Calculate the projectile's position at a given time
    g = 9.8  # acceleration due to gravity (m/s^2)
    rad_angle = math.radians(angle)
    horizontal_distance = velocity * math.cos(rad_angle) * time
    vertical_distance = (velocity * math.sin(rad_angle) * time) - (0.5 * g * time**2)
    return horizontal_distance, vertical_distance

def analyze_trajectory(velocity, angle):
    # Analyze the trajectory and create a list showing the projectile's position at regular time intervals
    time_intervals = [t / 10 for t in range(0, int((2 * velocity * math.sin(math.radians(angle))) / 9.8 * 10))]
    trajectory_data = []

    for time in time_intervals:
        position = calculate_position(velocity, angle, time)
        trajectory_data.append({"time": round(time, 2), "position": {"horizontal": round(position[0], 2), "vertical": round(position[1], 2)}})

    return trajectory_data

def calculate_max_distance(velocity, angle):
    # Calculate the maximum horizontal distance using the projectile motion equations
    g = 9.8  # acceleration due to gravity (m/s^2)
    rad_angle = math.radians(angle)
    max_distance = (velocity**2 * math.sin(2 * rad_angle)) / g
    return max_distance

def calculate_max_height(velocity, angle):
    # Calculate the maximum height using the projectile motion equations
    g = 9.8  # acceleration due to gravity (m/s^2)
    rad_angle = math.radians(angle)
    max_height = (velocity**2 * math.sin(rad_angle)**2) / (2 * g)
    return max_height

def analyze_trajectories(data):
    max_distances = []
    max_heights = []
    launches_exceeding_time_limit = []

    for launch in data['launches']:
        velocity = launch['velocity']
        angle = launch['angle']

        max_distance = calculate_max_distance(velocity, angle)
        max_distances.append((launch['index'], max_distance))

        max_height = calculate_max_height(velocity, angle)
        max_heights.append((launch['index'], max_height))

        flight_time = (2 * velocity * math.sin(math.radians(angle))) / 9.8
        if flight_time > 5:
            launches_exceeding_time_limit.append((launch['index'], flight_time))

    return max_distances, max_heights, launches_exceeding_time_limit

def read_input_file(json_data):
    # Cargar datos desde la cadena JSON
    data = json.loads(json_data)

    for launch in data['launches']:
        launch['velocity'] = float(launch['velocity'])
        launch['angle'] = float(launch['angle'])

    return data

def save_trajectory_data(trajectory_data, output_file):
    # Save trajectory data in JSON format
    with open(output_file, 'w') as file:
        json.dump(trajectory_data, file, indent=2)

def main():
    layout = [
        [sg.Text("Projectile Trajectory Analyzer", font=("Helvetica", 16))],
        [sg.Button("Analyze"), sg.Button("Analyze Trajectory"), sg.Button("Exit")],
        [sg.Output(size=(60, 10))]
    ]

    window = sg.Window("Projectile Trajectory Analyzer", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Analyze":
            try:
                data = read_input_file(json_data)
                max_distances, max_heights, launches_exceeding_time_limit = analyze_trajectories(data)

                print("\nResults:")
                print("Max Distances:")
                for index, distance in max_distances:
                    print(f"Launch {index}: {distance} meters")

                print("\nMax Heights:")
                for index, height in max_heights:
                    print(f"Launch {index}: {height} meters")

                print("\nLaunches Exceeding Time Limit (5 seconds):")
                for index, flight_time in launches_exceeding_time_limit:
                    print(f"Launch {index}: {flight_time} seconds")

            except Exception as e:
                print(f"Error: {e}")

        if event == "Analyze Trajectory":
            try:
                data = read_input_file(json_data)
                for launch in data['launches']:
                    velocity = launch['velocity']
                    angle = launch['angle']
                    trajectory_data = analyze_trajectory(velocity, angle)
                    output_file = f"trajectory_launch_{launch['index']}.json"
                    save_trajectory_data(trajectory_data, output_file)
                    print(f"Trajectory data for Launch {launch['index']} saved to {output_file}")

            except Exception as e:
                print(f"Error: {e}")

    window.close()

if __name__ == "__main__":
    main()
