import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import os
import sys 

influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBReader import InfluxDBReader
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
from InfluxDBMeasurement import InfluxDBMeasurement

class CorrelationCalculator(InfluxDBMeasurement):
    def __init__(self, bucket_configs):
        super().__init__()
        self.reader = InfluxDBReader()
        self.correlations = {}
        self.variables_array = {}

    def read_data_from_bucket(self, bucket_config):
        bucket_name = bucket_config['bucket_name']
        time_frame = bucket_config['time_frame']
        time_interval = bucket_config['time_interval']

        bucket_data = self.reader.read_from_bucket(bucket_name, time_frame, time_interval)
        bucket_dataframe = self.reader.query_result_to_dataframe(bucket_data)
        # print(bucket_dataframe)

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
        # print(formatted_power_consumption_array)

    def process_historical_weather_dataframe(self, bucket_dataframe):
        selected_fields = ['daily_rainfall_total', 'maximum_temperature', 'minimum_temperature', 'mean_temperature']
        averages = {}

        # Calculate average values for each selected weather field
        for field in selected_fields:
            field_data = bucket_dataframe[bucket_dataframe['_field'] == field]
            field_averages = field_data.groupby(['year', 'month'])['_value'].mean().values.astype(float)
            averages[field] = field_averages

        return averages
        # print(averages)

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
        # print(averages)

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
        # print(averages)

    def calculate_historical_correlations(self, data_array):
        correlations = {}

        for variable1_name, variable1_array in data_array.items():
            for variable2_name, variable2_array in data_array.items():
                correlation, _ = pearsonr(variable1_array, variable2_array)
                correlation = round(correlation, 2)
                key = f'{variable1_name} vs {variable2_name}'
                correlations[key] = correlation

        self.correlations = correlations

    def print_historical_correlations(self):
        # Print the correlation results
        for key, correlation in self.correlations.items():
            print(f'Correlation between {key}: {correlation}')

    def set_fields(self):
        pass

    def set_tags(self):
        pass