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
    """Converts a correlation matrix into a heatmap"""
    def __init__(self, correlations:dict):
        self.correlations = correlations

    def create_correlation_matrix(self):
        self.labels = self.get_labels()
        correlation_matrix = np.zeros((len(self.labels), len(self.labels)))
        for key, value in self.correlations.items():
            var1, var2 = key.split(' vs ')
            i = self.labels.index(var1)
            j = self.labels.index(var2)
            correlation_matrix[i, j] = value
        return correlation_matrix

    def plot_heatmap(self, ax, fontsize=12):
        num_variables = self.correlation_matrix.shape[0]
        heatmap = ax.imshow(self.correlation_matrix, cmap='coolwarm')
        cbar = plt.colorbar(heatmap, ax=ax, shrink=0.6, aspect=30, pad=0.02)
        ax.set_xticks(np.arange(num_variables))
        ax.set_yticks(np.arange(num_variables))
        ax.set_xticklabels(np.arange(num_variables) + 1, ha='right', fontsize=fontsize)
        ax.set_yticklabels(np.arange(num_variables) + 1, fontsize=fontsize)
        ax.set_aspect('equal')

        # Add correlation values to the heatmap
        for i in range(num_variables):
            for j in range(num_variables):
                text = ax.text(j, i, np.round(self.correlation_matrix[i, j], 2),
                               ha="center", va="center", color="black", fontsize=fontsize-2)

    def plot_table(self, ax, fontsize=12):
        table_data = [['ID', 'Variable']]
        for i, var in enumerate(self.labels):
            table_data.append([f"{i + 1}", var])
        table = ax.table(cellText=table_data, cellLoc='center', loc='center', bbox=[0, 0, 1, 1], colWidths=[0.1, 0.9])
        table.auto_set_font_size(False)
        table.set_fontsize(fontsize)
        for key, cell in table.get_celld().items():
            if key[0] == 0:  # Header cells
                cell.set_text_props(weight='bold', ha='center')
                cell.set_edgecolor('black')
                cell.set_linewidth(2)
            else:  # Data cells
                cell.set_edgecolor('gray')
                cell.set_linewidth(1.5)
        ax.axis('off')

    def plot_correlation_matrix(self, title="Correlation Matrix", fontsize=12):
        self.correlation_matrix = self.create_correlation_matrix()
        fig, axs = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [8, 1]}, figsize=(8, 10))
        axs[0].set_title(title)
        self.plot_heatmap(axs[0], fontsize)
        self.plot_table(axs[1], fontsize)
        plt.tight_layout()  # Adjust subplot parameters to give specified padding.
        output_path = os.path.join(OUTPUT_DIRECTORY, title)
        plt.savefig(output_path)

    def get_labels(self):
        variables = set()
        for key in self.correlations.keys():
            var1, var2 = key.split(' vs ')
            variables.add(var1)
            variables.add(var2)
        return sorted(variables)

    
def set_dynamic_title(self, ax, title, fontsize):
    # Calculate the appropriate font size based on the length of the title text
    title_fontsize = min(16, max(10, fontsize - 2 * len(title)))

    # Set the title with the dynamic font size
    ax.set_title(title, fontsize=title_fontsize)
    
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
        # Get the indexes of rows where 'weather_main' is in the '_field' column
        rows_to_drop = bucket_dataframe[bucket_dataframe['_field'].str.contains('weather_main')].index

        # Drop the rows with the specified indexes
        filtered_dataframe = bucket_dataframe.drop(index=rows_to_drop)
        
        averages = {}

        # Convert '_time' column to datetime type
        filtered_dataframe['_time'] = pd.to_datetime(filtered_dataframe['_time'])

        # Calculate daily average values for each remaining weather field
        for field in filtered_dataframe['_field'].unique():
            field_data = filtered_dataframe[filtered_dataframe['_field'] == field]
            daily_averages = field_data.groupby(filtered_dataframe['_time'].dt.date)['_value'].mean().values.astype(float)
            averages[field] = daily_averages

        return averages

    def process_dataframe(self, bucket_name, bucket_dataframe):
        # Convert '_time' column to datetime type
        bucket_dataframe['_time'] = pd.to_datetime(bucket_dataframe['_time'])

        # Combine all values from different measurements into one list
        combined_values = bucket_dataframe.groupby(bucket_dataframe['_time'].dt.date)['_value'].apply(list).values.tolist()

        # Calculate the average for each date
        averages = [np.mean(values) for values in combined_values]

        # Create a dictionary with the key based on the bucket name. eg: 'Daily Average Indoor Temperature'
        result = {f'Daily Average Farm {bucket_name}': averages}

        return result

    def format_correlation_key(self, variable_1, variable_2) -> str:
        """Returns a correlation key - keys will be in the format of variable_1 vs variable_2"""
        return f'{variable_1} vs {variable_2}' 

    def calculate_correlations(self, data_array) -> dict: 
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

    def print_correlations(self):
        for key, correlation in self.correlations.items():
            print(f'{key}: {correlation}')
