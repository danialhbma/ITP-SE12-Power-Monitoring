import os 
import sys 
influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import mean_absolute_error
import numpy as np 

# Set paths to the CSV files
temperature_file_path = os.path.join("data", "Temperature.csv")
weather_api_file_path = os.path.join("data", "WeatherAPI.csv")

# Initialize the data frame handler from InfluxDB
df_handler = InfluxDBDataFrameHandler()

# Load the data from CSV files
open_weather_map = df_handler.load_from_csv(weather_api_file_path)
farm_temperature_df = df_handler.load_from_csv(temperature_file_path)

# Select only the temperature data from the weather data
external_temperature_df = open_weather_map[open_weather_map["_field"] == "temperature"]

# Convert the '_time' column to datetime format and set it as index for both data frames
farm_temperature_df['_time'] = pd.to_datetime(farm_temperature_df['_time'])
farm_temperature_df.set_index('_time', inplace=True)
external_temperature_df['_time'] = pd.to_datetime(external_temperature_df['_time'])
external_temperature_df.set_index('_time', inplace=True)

# Resample the data frames to get hourly averages
farm_temperature_resampled = farm_temperature_df.resample('H').mean()
external_temperature_resampled = external_temperature_df.resample('H').mean()

# Merge the two data frames on the index (which is the '_time' column)
combined_df = pd.merge(farm_temperature_resampled, external_temperature_resampled, 
                       left_index=True, right_index=True, suffixes=('_internal', '_external'))

# Fill any missing values in the data frame with the mean value of the respective column
combined_df.fillna(combined_df.mean(), inplace=True)

# Prepare the data for linear regression
X = combined_df['_value_external'].values.reshape(-1,1)  # Feature: external temperature
y = combined_df['_value_internal'].values.reshape(-1,1)  # Target: internal temperature

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train a linear regression model
regressor = LinearRegression()  
regressor.fit(X_train, y_train)

# Print the intercept and coefficient of the linear regression model
print("Intercept: ", regressor.intercept_)
print("Slope: ", regressor.coef_)

# Use the trained model to make predictions on the testing set
y_pred = regressor.predict(X_test)

# Compare the actual and predicted internal temperatures for the testing set
df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
print(df.head())

# Calculate the mean absolute error of the predictions
mae = mean_absolute_error(y_test, y_pred)
print('Mean Absolute Error:', mae)


# Generating a range of external temperatures
external_temp_range = np.linspace(25, 40, 100).reshape(-1,1)

# Predicting internal temperatures for this range
predicted_internal_temp = regressor.predict(external_temp_range)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(external_temp_range, predicted_internal_temp, color='blue', label='Predicted Internal Temp')
plt.title('Predicted Internal Temperature based on External Temperature')
plt.xlabel('External Temperature (°C)')
plt.ylabel('Predicted Internal Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()