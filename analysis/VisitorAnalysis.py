import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone

def read_ambient_data(file_path):
    df = pd.read_csv(file_path, usecols=["_time", "_value", "_measurement"])
    ambient_data = [(convert_to_datetime(row["_time"]), row["_value"]) for _, row in df.iterrows() if "rack" in row["_measurement"]]
    return ambient_data

def read_temperature_data(file_path):
    df = pd.read_csv(file_path, usecols=["_time", "_value", "_measurement"])
    temperature_data = [(convert_to_datetime(row["_time"]), {row["_measurement"]: row["_value"]}) for _, row in df.iterrows() if "rack" in row["_measurement"]]
    return temperature_data

def convert_to_datetime(time_str):
    return datetime.fromisoformat(time_str.replace("Z", "+00:00"))

def generate_visitors_graph(ambient_file, temperature_file, output_dir):
    # Read ambient light data
    ambient_data = read_ambient_data(ambient_file)

    # Read temperature data
    temperature_data = read_temperature_data(temperature_file)

def generate_visitors_graph(ambient_file, temperature_file, output_dir):
    ambient_data = read_ambient_data(ambient_file)
    temperature_data = read_temperature_data(temperature_file)

    # Analyze ambient data to determine visits
    visits = []
    visit_start_time = None
    for time, light_reading in ambient_data:
        if light_reading > 600:
            if visit_start_time is None:
                visit_start_time = time
        else:
            if visit_start_time is not None:
                visits.append((visit_start_time, time))
                visit_start_time = None

    # Generate a graph showing the effects of visitors
    fig, ax1 = plt.subplots()

    # Plot ambient light data
    times, light_readings = zip(*ambient_data)
    ax1.plot(times, light_readings, 'b-', label='Ambient Light')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Light Reading', color='b')
    ax1.tick_params('y', colors='b')
    ax1.axhline(y=600, color='r', linestyle='--', label='Threshold')

    # Plot temperature data for each rack
    for i in range(1, 5):
        rack_temperatures = [(time, temp[f"rack{i}_temperature"]) for time, temp in temperature_data if isinstance(temp, dict) and f"rack{i}_temperature" in temp]
        times, temperatures = zip(*rack_temperatures)
        ax2 = ax1.twinx()
        ax2.plot(times, temperatures, label=f'Rack {i} Temperature')

    # Plot visits as vertical lines
    for visit_start, visit_end in visits:
        ax1.axvline(x=visit_start, color='orange', linestyle='-', linewidth=2, label='Visit')
        ax1.axvline(x=visit_end, color='orange', linestyle='-', linewidth=2)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    # Save the graph to the output directory
    plt.savefig(f"{output_dir}/visitors_graph.png")
    plt.show()

ambient_file_path = 'data/ambient.csv' 
temperature_file_path = 'data/temperature.csv' 
output_directory = 'results' 

generate_visitors_graph(ambient_file_path, temperature_file_path, output_directory)
