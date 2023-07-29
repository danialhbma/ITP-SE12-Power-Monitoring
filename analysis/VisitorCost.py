import pandas as pd
import os 

def read_csv(file_path, columns):
    return pd.read_csv(file_path, usecols=columns)

def get_measurement_label(measurement):
    if measurement.startswith('rack') and measurement.endswith('_temperature'):
        parts = measurement.split('_')
        rack_number = parts[0][4:]  # Get the rack number from the measurement
        return f"Rack {rack_number}"
    return measurement

# Read Ambient.csv
ambient_df = read_csv(os.path.join("data", "Ambient.csv"), ['_time', '_value'])

# Read Temperature.csv
temperature_df = read_csv(os.path.join("data", "Temperature.csv"), ['_time', '_value', '_measurement'])

# Filter Ambient.csv data with _value above 600 (Visit detection)
ambient_above_600_df = ambient_df[ambient_df['_value'] > 600]

# Find intersections (Check if the visit caused an increase in temperature)
intersections_df = pd.merge(ambient_above_600_df, temperature_df, on='_time', suffixes=('_ambient', '_temperature'))

if not intersections_df.empty:
    # Print intersections
    for _, row in intersections_df.iterrows():
        print(f"There was a visit to the farm at {row['_time']}.")

        # Find multiple instances at the same _time (multiple racks)
        temperature_instances = intersections_df[intersections_df['_time'] == row['_time']]
        for _, temp_row in temperature_instances.iterrows():
            measurement = get_measurement_label(temp_row['_measurement'])
            print(f"The temperature of the container at {measurement} was {temp_row['_value_temperature']}C.")

    # Technically, the aircon temperature should be taken into account for the extra cost incurred due to the visit.
    # However, since the unit is a non-inverter, there were no extra charges incurred. This part is a proof of concept.
    # In the event of an inverter aircon, the temperature of the aircon should be calculated here.

    # Calculate the visit cost
    start_time = ambient_above_600_df['_time'].min()
    end_time = ambient_above_600_df['_time'].max()

    visit_duration_minutes = (pd.to_datetime(end_time) - pd.to_datetime(start_time)).total_seconds() / 60
    visit_duration_hours = visit_duration_minutes / 60

    P = 0.17 * 220 # P = I * V
    kwh_value = (P * visit_duration_hours)/1000 # kWh = (P * t)/1000
    cost = kwh_value * 0.29

    print(f"The visit lasted {visit_duration_minutes:.2f} minutes.")
    print(f"The visit cost an extra ${cost:.2f}.")
else:
    print("No intersections found.")
