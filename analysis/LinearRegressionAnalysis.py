import os
import joblib
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from pytz import timezone
from datetime import time, datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

TIMEZONE = timezone('Asia/Singapore')
# CSV paths
PC_CSV = 'analysis/data/Power Consumption.csv'
MODEL_PATH = 'analysis/model/pc_linear_regression_model.pkl'
PREDICTIONS_CSV = 'analysis/data/monthly_predictions.csv'

''' data_preprocessing function is used to process the 
    csv file and handle any missing data accordingly '''
def data_preprocessing(csv_file):
    # Read the CSV file and handle any missing values
    power_consumption = pd.read_csv(csv_file)

    # Select the desired columns
    power_consumption = power_consumption[['device_name', '_time', '_value']]

    # Convert the _time column to datetime (so that we can filter/group/sort on the column) and timezone (since csv is not in SG timezone)
    power_consumption['_time'] = pd.to_datetime(power_consumption['_time']).dt.tz_convert(TIMEZONE)

    # Initialize an empty DataFrame to store the processed data
    processed_data = pd.DataFrame()

    # Get the unique device names
    devices = power_consumption['device_name'].unique()

    for device_name in devices:
        # Filter data for the specified device_name
        device_data = power_consumption.loc[power_consumption['device_name'] == device_name]

        # Fill missing timestamps with NaN
        time_range = pd.date_range(start=device_data['_time'].min(), end=device_data['_time'].max(), freq='H')
        device_data = device_data.set_index('_time').reindex(time_range).reset_index().rename(columns={'index': '_time'})

        # Filter based on device type as each has their own operating hours
        if 'Light' in device_name:
            # Define the time range for light devices (Rack 2 & 3 - 7am to 7pm, Rack 1 - 3am to 3pm)
            light_time_range = (time(7, 0), time(19, 0)) if device_name in ['Rack 3 Light', 'Rack 2 Light'] else (time(3, 0), time(15, 0))

            # Create a mask for missing values within the light time range
            time_mask = device_data['_time'].dt.time.between(*light_time_range)

            # Perform forward fill and backward fill (on those within the time range specified)
            device_data.loc[time_mask & device_data['_value'].isna(), '_value'] = device_data['_value'].ffill().bfill()

            # Fill missing values outside the light time range with 0.9
            device_data.loc[~time_mask & device_data['_value'].isna(), '_value'] = 0.9

        elif 'Water' in device_name: 
            # Backward or Forward fill missing values
            device_data['_value'] = device_data['_value'].ffill().bfill()

        # Replace remaining NaN device_name with the specified device_name
        device_data['device_name'].fillna(device_name, inplace=True)

        # Concatenate device_data with processed_data
        processed_data = pd.concat([processed_data, device_data])

    return processed_data

''' get_daily_values function is used to split the dataframe based
    on the device type (Light, Timer & Water), calculate
    their daily values and combine them back into 1 dataframe'''
def get_daily_values(dataframe):
    # Get daily power consumption for each device in Watts (W)
    # Convert _time column to datetime
    dataframe['_time'] = pd.to_datetime(dataframe['_time'])

    # Separate light, timer, and water values into separate DataFrames
    light_values = dataframe[(dataframe['device_name'].str.contains('Light')) & (dataframe['_value'] > 2)]
    timer_values = dataframe[dataframe['device_name'].str.contains('Light')]
    water_values = dataframe[dataframe['device_name'].str.contains('Water')]

    # Subtract the average timer value from the light value
    light_values.loc[:, '_value'] = light_values['_value'] - 0.9
    # Replace the value with the average timer value (since light and timer values are combined when lights are on)
    timer_values.loc[timer_values['_value'] > 2, '_value'] = 0.9

    # Calculate daily power consumption for light values
    light_daily = light_values.groupby([light_values['_time'].dt.date, 'device_name'])['_value'].sum().reset_index()

    # Calculate daily power consumption for timer values and replace the device name (eg: Rack 1 Light to Rack 1 Timer)
    timer_values.loc[:, 'device_name'] = timer_values['device_name'].str.replace('Light', 'Timer')
    timer_daily = timer_values.groupby([timer_values['_time'].dt.date, 'device_name'])['_value'].sum().reset_index()

    # Calculate daily power consumption for water values
    water_daily = water_values.groupby([water_values['_time'].dt.date, 'device_name'])['_value'].sum().reset_index()

    # Concatenate the light, timer, and water daily DataFrames
    merged_daily = pd.concat([light_daily, timer_daily, water_daily])

    return merged_daily

''' data_preparation function is used to prepare the necessary 
    variables (x, y) for linear regression model training'''
def data_preparation(dataframe):
    # Get the daily average dataframe
    averaged_dataframe = get_daily_values(dataframe)

    # Convert _time column to datetime
    averaged_dataframe['_time'] = pd.to_datetime(averaged_dataframe['_time'])

    # Extract the date components (Feature Extraction)
    averaged_dataframe['day_of_month'] = averaged_dataframe['_time'].dt.day
    averaged_dataframe['month'] = averaged_dataframe['_time'].dt.month

    # Encode categorical variables
    averaged_dataframe_encoded = pd.get_dummies(averaged_dataframe, columns=['device_name'])

    # Exclude unnecessary columns
    features = averaged_dataframe_encoded.drop(['_value', '_time'], axis=1).columns.tolist()

    # Set the x and y variables
    x = averaged_dataframe_encoded[features]
    y = averaged_dataframe_encoded['_value']

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test, features

''' model_training function is used to train new model or 
    retrain a model whenever needed'''
def model_training(x_train, x_test, y_train, y_test):
    # Use this method whenever model needs to be refitted or if model doesn't exists
    # Create instance of LinearRegression class
    model = LinearRegression()

    # Fit the model using the training set
    model.fit(x_train, y_train)

    # Use the model to make predictions on test set
    y_pred = model.predict(x_test)

    # Save the model to a file
    joblib.dump(model, MODEL_PATH)

    # # Evaluate the model's performance
    # mse = mean_squared_error(y_test, y_pred)
    # r2 = r2_score(y_test, y_pred)
    # mae = mean_absolute_error(y_test, y_pred)

    # print("Mean Squared Error:", mse)
    # print("R-squared:", r2)
    # print("Mean Absolute Error:", mae)

    # residuals = y_test - y_pred

    # # Plotting the residuals
    # plt.scatter(y_pred, residuals)
    # plt.axhline(y=0, color='r', linestyle='--')
    # plt.xlabel("Predicted Values")
    # plt.ylabel("Residuals")
    # plt.title("Residual Analysis")
    # plt.show()

''' formatted_test_model_predictions function is used to test out
    the predictions of model and display it a formatted dataframe
    for readability'''
def formatted_test_model_predictions(model, x_test):
    # This is to view the model predictions on x_test in a readable format (Maps the predictions to respective device, day and month)
    # sort the x_test by the 'day of month' and 'month' column
    x_test_sorted = x_test.sort_values(by=["month", "day_of_month"])

    # Load the linear regression model
    loaded_model = joblib.load(model)

    # Use the loaded model for predictions
    predictions = loaded_model.predict(x_test_sorted)

    # Create a list to store the device names, day_of_month and month
    device_names = []
    days_of_month = []
    months = []

    # Collect the device names and day of the month from x_test_sorted
    for i, row in x_test_sorted.iterrows():
        for column, value in row.items():
            if value:
                if column == 'day_of_month':
                    days_of_month.append(value)
                elif column == 'month':
                    months.append(value)
                else:
                    # To get only the device name (eg: Rack 1 Light)
                    device_name = column.replace("device_name_", "")
                    device_names.append(device_name)

    # Create a DataFrame with device_names, days_of_month, and predictions
    result_df = pd.DataFrame({'Month': months, 'Day of Month': days_of_month, 'Device Name': device_names, 'Prediction': predictions})

    return result_df

''' get_monthly_predictions function is used to predict the daily
    values of each device for the entire month'''
def get_monthly_predictions(model, features):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Get the range of days for the current month
    _, num_days = calendar.monthrange(current_year, current_month)

    # Create a list to store the rows
    rows = []

    # Iterate over each device name
    for feature in features:
        if feature.startswith('device_name_'):
            # Iterate over each day
            for day in range(1, num_days + 1):
                # Create a dictionary to store the values for the current row
                row = {'day_of_month': day, 'month': current_month}
                
                # Set the device_name feature value
                row[feature] = True
                
                # Set the other feature values
                for other_feature in features:
                    if other_feature == feature or other_feature == 'day_of_month' or other_feature == 'month':
                        continue
                    row[other_feature] = False
                
                # Append the row to the list
                rows.append(row)

    # Create the DataFrame from the rows
    predictions_df = pd.DataFrame(rows)

    # Load the trained model from the file
    loaded_model = joblib.load(model)

    # Make predictions using the trained model for each row in predictions_df
    predictions = loaded_model.predict(predictions_df)

    # Assign the predictions to the 'Prediction' column in predictions_df
    predictions_df['Prediction'] = predictions

    # Call the modify_dataframe function to tidy up the DataFrame
    monthly_predictions_df = format_dataframe(predictions_df)

    # export the dataframe as a csv
    monthly_predictions_df.to_csv(PREDICTIONS_CSV, index=False)

    print('monthly_predictions.csv created')

''' format_dataframe function is used to format the dataframe for readability'''
def format_dataframe(df):
    # Create a list to store the device names, day_of_month and month
    device_names = []
    days_of_month = []
    months = []
    predictions = []

    # Collect the device names and day of the month from x_test_sorted
    for i, row in df.iterrows():
        for column, value in row.items():
            if value:
                if column == 'day_of_month':
                    days_of_month.append(value)
                elif column == 'month':
                    months.append(value)
                elif column == 'Prediction':
                    predictions.append(value)
                else:
                    device_name = column.replace("device_name_", "")
                    device_names.append(device_name)

    # Create a DataFrame with device_names, days_of_month, and predictions
    result_df = pd.DataFrame({'Month': months, 'Day of Month': days_of_month, 'Device Name': device_names, 'Prediction': predictions})

    return result_df

# Check if csv file exists
if os.path.isfile(PC_CSV):
    processed_data = data_preprocessing(PC_CSV)
    x_train, x_test, y_train, y_test, features = data_preparation(processed_data)
    # Check if the model exists
    if os.path.isfile(MODEL_PATH):
        get_monthly_predictions(MODEL_PATH, features)
    else:
        model_training(x_train, x_test, y_train, y_test)
        get_monthly_predictions(MODEL_PATH, features)
else:
    print("CSV file doesn't exist")    