import os
import pandas as pd
from CorrelationCalculator import CorrelationCalculator, CorrelationPlotter

# CSV file
EDPC_CSV = 'daily_estimated_pc.csv'

''' MonthlyCorrelation script will do 2 things:
    1. Correlate the external weather conditions (WeatherAPI) & internal farm conditions (Temperature & Humidity)
        & produce a heatmap of the result
    2. Correlate the external weather conditions & internal farm conditions & power consumption (daily_estimated_pc.csv)
        & separate out the weak correlations before producing the heatmap'''

# Define the bucket configurations (1st & 2nd correlation uses the same bucket)
bucket_configs = [
    {
        'bucket_name': 'WeatherAPI',
        'time_frame': '30d',
        'time_interval': '30m'
    },
        {
        'bucket_name': 'Temperature',
        'time_frame': '30d',
        'time_interval': '30m'
    },
    {
        'bucket_name': 'Humidity',
        'time_frame': '30d',
        'time_interval': '30m'
    }
    # Add more bucket configurations if needed
]

''' 1st Correlation '''
def Correlate_ExtCond_To_IntCond(result):
    calculator.calculate_correlations(result)
    # calculator.print_correlations()

    plotter = CorrelationPlotter(calculator.correlations)
    plotter.plot_correlation_matrix("WeatherAPI & Farm Conditions")

''' 2nd Correlation '''
def Correlate_ExtCond_To_IntCond_To_FPC(result):
    ''' To get the daily power consumption data from the csv,
    store the into alist and then combine them to the array
    that is the parameter of the correlation calculations'''

    # Get the current directory of the Python script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file in the sub_directory
    csv_file_path = os.path.join(current_directory, "data", EDPC_CSV)
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    # Get the estimated daily power consumption column only
    daily_power_consumption = df['Estimated Daily Power Consumption (kWh)']
    # Convert the column to a list using tolist()
    daily_power_consumption_list = daily_power_consumption.tolist()
    # Add the daily_power_consumption list to the result array
    result['Daily Farm Power Consumption'] = daily_power_consumption_list

    calculator.calculate_correlations(result)
    # calculator.print_correlations()
    # calculator.remove_weak_correlation()

    plotter = CorrelationPlotter(calculator.correlations)
    plotter.plot_correlation_matrix("Correlation between farm environmental conditions to estimated power consumption")

# Create an instance of the CorrelationCalculator
calculator = CorrelationCalculator(bucket_configs)

# Read and process data from each bucket
for bucket_config in bucket_configs:
    result = calculator.read_data_from_bucket(bucket_config)

# Correlate_ExtCond_To_IntCond(result)
Correlate_ExtCond_To_IntCond_To_FPC(result)