import pandas as pd
import calendar
import datetime
import os
from tabulate import tabulate

PREDICTIONS_CSV = 'analysis/data/monthly_predictions.csv'
RACK_EMPC_CSV = 'analysis/data/rack_EMPC.csv'
# Senoko's electricity rate per kWh in SGD
ELECTRICITY_RATE = 28.98 / 100 

def get_rack_empc():
    # read the csv file
    predictions_df = pd.read_csv(PREDICTIONS_CSV)
    rack_df = pd.read_csv(RACK_EMPC_CSV)

    # get the estimated monthly power consumption (empc) of each device in Watts (W)
    predictions_df = predictions_df.groupby('Device Name')['Prediction'].sum().reset_index()
    # rename the column to estimated power consumption (epc)
    predictions_df = predictions_df.rename(columns={'Prediction': 'Estimated Power Consumption'})

    # combined the 2 dataframe
    combined_df = pd.concat([predictions_df, rack_df], ignore_index=True)
    combined_df = predictions_df.combine_first(rack_df)

    # Iterate over each row in the DataFrame
    for index, row in combined_df.iterrows():
        # find rows with 0 epc
        if row['Estimated Power Consumption'] == 0:
            similar_device_type = row['Device Name'].split(' ')[-1]
            # first find similar row based on their plant type and device type
            similar_rows = combined_df[(combined_df['Rack No'] != row['Rack No']) &
                                    (combined_df['Plant Type'] == row['Plant Type']) &
                                    (combined_df['Device Name'].str.endswith(similar_device_type))]
            # if no similar rows, then find one based on their growth
            if similar_rows.empty:
                similar_rows = combined_df[(combined_df['Rack No'] != row['Rack No']) &
                                        (combined_df['Growth'] == row['Growth']) &
                                        (combined_df['Device Name'].str.endswith(similar_device_type))]
            # if have similar rows, then set the row's epc with the same value as the similar_row's epc
            if not similar_rows.empty:
                similar_row = similar_rows.iloc[0]
                combined_df.at[index, 'Estimated Power Consumption'] = similar_row['Estimated Power Consumption']

    return combined_df

def get_other_empc():
    # Get the current date
    current_date = datetime.datetime.now()

    # Extract the current year and month
    year = current_date.year
    month = current_date.month

    # Get the number of days in the current month
    num_days = calendar.monthrange(year, month)[1]

    # empc based on each device's specifications, operating hours and number of days

    # Indoor aircon unit (operating input + indoor fan motor)
    indoor_aircon_empc = (1230 + 58) * 24 * num_days 
    # Outdoor aircon unit (compressor + outdoor fan motor)
    outdoor_aircon_empc = (1970 + 58) * 24 * num_days 
    # to be updated once more data for ambient comes in
    ceiling_light_empc = 36 * 1 * num_days

    return indoor_aircon_empc, outdoor_aircon_empc, ceiling_light_empc

def calculate_cost(): 
    # call methods to get the empc of each device
    rack_empc = get_rack_empc()
    indoor_aircon_empc, outdoor_aircon_empc, ceiling_light_empc = get_other_empc()

    # Extract the "Device Name" and "Estimated Power Consumption" columns
    result_df = rack_empc[['Device Name', 'Estimated Power Consumption']]

    # Create a copy of the dataframe
    result_df = result_df.copy()

    # Modify the copied dataframe
    result_df.loc[:, 'Estimated Power Consumption (kWh)'] = (result_df['Estimated Power Consumption'] / 1000).round(2)
    result_df.loc[:, 'Cost ($)'] = (result_df['Estimated Power Consumption (kWh)'] * ELECTRICITY_RATE).round(2)

    # Drop the "Estimated Power Consumption" column
    result_df = result_df.drop('Estimated Power Consumption', axis=1)

    # Get Indoor Aircons'/Outdoor Aircons'/Ceiling Lights' epc in kWh
    indoor_aircon_epc_kwh = round(indoor_aircon_empc / 1000, 2)
    outdoor_aircon_epc_kwh = round(outdoor_aircon_empc / 1000, 2)
    ceiling_light_epc_kwh = round(ceiling_light_empc / 1000, 2)

    # Calculate the cost of indoor_aircon_epc_kwh/outdoor_aircon_epc_kwh/ceiling_light_epc_kwh
    indoor_aircon_cost = round(indoor_aircon_epc_kwh * ELECTRICITY_RATE, 2)
    outdoor_aircon_cost = round(outdoor_aircon_epc_kwh * ELECTRICITY_RATE, 2)
    ceiling_light_cost = round(ceiling_light_epc_kwh * ELECTRICITY_RATE, 2)

    # Create a dictionary to store the other devices' data (device name, epc in kWh and cost)
    other_device_data = {'Device Name': ['Indoor Aircon Unit 1', 'Indoor Aircon Unit 2', 'Outdoor Aircon Unit 1', 'Ceiling Lights'],
                          'Estimated Power Consumption (kWh)': [indoor_aircon_epc_kwh, indoor_aircon_epc_kwh, outdoor_aircon_epc_kwh, ceiling_light_epc_kwh],
                          'Cost ($)': [indoor_aircon_cost, indoor_aircon_cost, outdoor_aircon_cost, ceiling_light_cost]}
    
    # Make it into a dataframe
    other_device_df = pd.DataFrame(other_device_data)

    # Combine the 2 dataframes together 
    result_df = pd.concat([result_df, other_device_df], ignore_index=True)

    # Display the result_df as a table
    result_table = tabulate(result_df, headers='keys', tablefmt='psql')

    # Print the table
    print(result_table)

# check if csv files exists
if os.path.isfile(PREDICTIONS_CSV) & os.path.isfile(RACK_EMPC_CSV):
    calculate_cost()
else:
    print("CSV files doesn't exist")