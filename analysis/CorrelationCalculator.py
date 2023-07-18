import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import os
import sys 
import matplotlib.pyplot as plt

influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBReader import InfluxDBReader
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler

# LIVE SERVER
URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"


# Output directory for plots
OUTPUT_DIRECTORY = "results"

class CorrelationPlotter():
    """Class responsible for parsing the correlations dictionary that CorrelationCalculator will provide"""
    def __init__(self, correlations:dict):
        """Assumes the correlations dictionary follows the format of {var 1 vs var 2}: {correlation_score}"""
        self.correlations = correlations
        
    def create_correlation_matrix(self):
        variables = list(set([key.split(' vs ')[0] for key in self.correlations]))

        # Create an empty correlation matrix
        correlation_matrix = np.zeros((len(variables), len(variables)))

        # Populate the correlation matrix
        for key, value in self.correlations.items():
            var1, var2 = key.split(' vs ')
            i = variables.index(var1)
            j = variables.index(var2)
            correlation_matrix[i, j] = value
        return correlation_matrix
    
    def plot_correlation_matrix(self, title="Correlation Matrix"):
        # Create correlation matrix
        self.correlation_matrix = self.create_correlation_matrix()

        # Get the number of variables
        num_variables = self.correlation_matrix.shape[0]

        # Generate tick labels based on the variable indices
        tick_labels = self.get_labels()

        # Create the figure and axes
        fig, axs = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [10, 1]}, figsize=(8, 10))

        # Create the heatmap
        heatmap = axs[0].imshow(self.correlation_matrix, cmap='coolwarm')

        # Add colorbar
        cbar = plt.colorbar(heatmap, ax=axs[0], shrink=0.6, aspect=30, pad=0.02)

        # Set tick labels and positions
        axs[0].set_xticks(np.arange(num_variables))
        axs[0].set_yticks(np.arange(num_variables))
        axs[0].set_xticklabels(np.arange(num_variables) + 1, rotation=45, ha='right')
        axs[0].set_yticklabels(np.arange(num_variables) + 1)

        # Center the heatmap
        axs[0].set_aspect('equal')

        # Set title
        axs[0].set_title(title)

        # Create a table for variable legend
        table_data = [['ID', 'Variable']]
        for i, var in enumerate(tick_labels):
            table_data.append([f"G{i + 1}", var])

        # Define table properties
        table = axs[1].table(cellText=table_data, colLabels=None, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

        # Set table properties
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)  # Adjust the scale to change the row height

        # Set cell alignment and borders
        for key, cell in table.get_celld().items():
            if key[0] == 0:  # Header cells
                cell.set_text_props(weight='bold', ha='center')
                cell.set_edgecolor('black')
                cell.set_linewidth(1)
            else:  # Data cells
                cell.set_edgecolor('gray')
                cell.set_linewidth(0.5)

        # Hide ticks and labels for table
        axs[1].axis('off')
        output_path = os.path.join(OUTPUT_DIRECTORY, title)
        plt.savefig(output_path)

    """
    def plot_correlation_matrix(self, title="correlations"):
        # Create correlation matrix
        self.correlation_matrix = self.create_correlation_matrix()

        # Get the number of variables
        num_variables = self.correlation_matrix.shape[0]

        # Generate tick labels based on the variable indices
        tick_labels = self.get_labels()

        # Create the figure and axes
        fig, ax = plt.subplots()

        # Create the heatmap
        heatmap = ax.imshow(self.correlation_matrix, cmap='coolwarm')

        # Add colorbar
        cbar = plt.colorbar(heatmap)

        # Set tick labels and positions
        ax.set_xticks(np.arange(num_variables))
        ax.set_xticklabels(tick_labels, rotation=45, ha="right")  # Rotate x-axis tick labels

        # Add padding between each label
        ax.set_yticks(np.arange(num_variables))
        ax.set_yticklabels(tick_labels)

        # Center the heatmap
        ax.set_aspect('equal')

        # Set title
        ax.set_title(title)

        # Adjust subplot parameters for a tight layout
        fig.tight_layout(pad=2.0)

        # Display the plot
        output_path = os.path.join(OUTPUT_DIRECTORY, title)
        plt.savefig(output_path)
    """
    def get_labels(self):
        # Extracts labels from the correlation dictionary
        variables = set()
        for key in self.correlations.keys():
            var1, var2 = key.split(' vs ')
            variables.add(var1)
            variables.add(var2)
        return sorted(variables)

class CorrelationCalculator():
    """
    Determines correlation between variables.
    Returns: correlations dictionary, where keys follow the format of
    {var1 vs var2}:{correlation_score}
    """
    def __init__(self, bucket_configs):
        self.reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG)
        self.correlations = {}
        self.variables_array = {}

    def read_data_from_bucket(self, bucket_config):
        bucket_name = bucket_config['bucket_name']
        time_frame = bucket_config['time_frame']
        time_interval = bucket_config['time_interval']

        bucket_data = self.reader.read_from_bucket(bucket_name, time_frame, time_interval)
        bucket_dataframe = self.reader.query_result_to_dataframe(bucket_data)

        if bucket_name == 'Historical Power Consumption':
             self.variables_array.update(self.process_historical_power_consumption_dataframe(bucket_dataframe))
        elif bucket_name == 'Historical Weather Data':
            self.variables_array.update(self.process_historical_weather_dataframe(bucket_dataframe))
        elif bucket_name == 'WeatherAPI':
            self.variables_array.update(self.process_weatherapi_dataframe(bucket_dataframe))
        else:
            self.variables_array.update(self.process_dataframe(bucket_name, bucket_dataframe))

        return self.variables_array
        
    def process_historical_power_consumption_dataframe(self, bucket_dataframe):
        # Sort the power consumption data by year and month
        sorted_dataframe = bucket_dataframe.sort_values(by=['year', 'month'])

        # Convert power consumption values to a float array
        power_consumption_array = sorted_dataframe['_value'].values.astype(float)

        # Add field name to the array
        field_name = sorted_dataframe['_field'].iloc[0]
        formatted_power_consumption_array = {field_name: power_consumption_array}

        return formatted_power_consumption_array

    def process_historical_weather_dataframe(self, bucket_dataframe):
        selected_fields = ['daily_rainfall_total', 'maximum_temperature', 'minimum_temperature', 'mean_temperature']
        averages = {}

        # Calculate average values for each selected weather field
        for field in selected_fields:
            field_data = bucket_dataframe[bucket_dataframe['_field'] == field]
            field_averages = field_data.groupby(['year', 'month'])['_value'].mean().values.astype(float)
            averages[field] = field_averages

        return averages
 
    def process_weatherapi_dataframe(self, bucket_dataframe):
        selected_fields = ['temp_max', 'temp_min', 'temperature']
        averages = {}

        # Convert '_time' column to datetime type
        bucket_dataframe['_time'] = pd.to_datetime(bucket_dataframe['_time'])

        # Calculate daily average values for each selected weather field
        for field in selected_fields:
            field_data = bucket_dataframe[bucket_dataframe['_field'] == field]
            daily_averages = field_data.groupby(bucket_dataframe['_time'].dt.date)['_value'].mean().values.astype(float)
            averages[field] = daily_averages

        return averages


    def process_dataframe(self, bucket_name, bucket_dataframe):
        # Convert '_time' column to datetime type
        bucket_dataframe['_time'] = pd.to_datetime(bucket_dataframe['_time'])

        # Combine all values from different measurements into one array
        combined_values = bucket_dataframe.groupby(bucket_dataframe['_time'].dt.date)['_value'].apply(list).values.tolist()

        # Calculate the average for each date
        averages = [np.mean(values) for values in combined_values]

        # Create a dictionary with the key based on the bucket name. eg: 'Daily Average Indoor Temperature'
        result = {f'Daily Average Farm {bucket_name}': averages}

        return result

    def format_correlation_key(self, variable_1, variable_2) -> str:
        """Returns a correlation key - keys will be in the format of variable_1 vs variable_2"""
        return f'{variable_1} vs {variable_2}' 

    def calculate_historical_correlations(self, data_array) -> dict: 
        """
        Creates and returns a correlations dictionary.
        {var1 vs var2}:{correlation}
        note that the naming of keys should follow this format as downstream applications will parse correlation matrix as such.
        """
        correlations = {}
        for variable1_name, variable1_array in data_array.items():
            for variable2_name, variable2_array in data_array.items():
                correlation, _ = pearsonr(variable1_array, variable2_array)
                correlation = round(correlation, 2)
                key = self.format_correlation_key(variable1_name, variable2_name)
                correlations[key] = correlation
        self.correlations = correlations
        return self.correlations

    def print_historical_correlations(self):
        for key, correlation in self.correlations.items():
            print(f'{key}: {correlation}')
