import pandas as pd
import calendar
import datetime
import os
import matplotlib.pyplot as plt


# Paths
DATA_DIR = 'data'
RESULTS_DIR = 'results'
PREDICTIONS_CSV = os.path.join(DATA_DIR, 'monthly_predictions.csv')
RACK_EMPC_CSV = os.path.join(DATA_DIR, 'rack_EMPC.csv')
EDPC_CSV = os.path.join(DATA_DIR, 'daily_estimated_pc.csv')
EMC_CSV = os.path.join(DATA_DIR, 'monthly_estimated_cost.csv')
OUTPUT_PNG_PATH = RESULTS_DIR

# Senoko's electricity rate per kWh in SGD
ELECTRICITY_RATE = 28.98 / 100 

''' Device Specifications '''
# Aircon (indoor & outdoor unit)
INDOOR_AIRCON_FAN = 120
OUTDOOR_AIRCON_FAN = 85
OUTDOOR_AIRCON_COOLING_MIN = 855
OUTDOOR_AIRCON_COOLING_MAX = 4795
OUTDOOR_AIRCON_COMPRESSOR_NORM = 2820
OUTDOOR_AIRCON_COMPRESSOR_MAX = 3040

# Ceiling Lights
CEILING_LIGHT_POWER = 36
NO_OF_LIGHTS = 6

class MonthlyCostCalculator():
    def __init__(self):
        pass
    
    ''' get_rack_empc function is used to get the estimated monthly
        power consumption (empc) of each device for each rack'''
    def get_rack_empc(self):
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

    ''' get_other_empc function is used to get the empc of other devices
        in the container that contributes to pc'''
    def get_other_empc(self):
        # Get the current date
        current_date = datetime.datetime.now()

        # Extract the current year and month
        year = current_date.year
        month = current_date.month
        month_in_str = current_date.strftime('%B')

        # Get the number of days in the current month
        num_days = calendar.monthrange(year, month)[1]

        # empc based on each device's specifications, number of devices (for lights), operating hours and number of days
        # Indoor aircon unit
        indoor_aircon_empc = INDOOR_AIRCON_FAN * 24 * num_days 
        # Outdoor aircon unit
        outdoor_aircon_empc = (((OUTDOOR_AIRCON_COOLING_MAX + OUTDOOR_AIRCON_COOLING_MIN)/2) + OUTDOOR_AIRCON_COMPRESSOR_NORM + OUTDOOR_AIRCON_FAN) * 24 * num_days  
        # to be updated once more data for ambient comes in
        ceiling_light_empc = CEILING_LIGHT_POWER * NO_OF_LIGHTS * 1 * num_days

        return indoor_aircon_empc, outdoor_aircon_empc, ceiling_light_empc, month_in_str, year

    ''' calculate_cost function is used to calculate the estimated monthly cost (emc) 
        of each device and displays the result (device, empc and cost)'''
    def calculate_cost(self): 
        # call functions to get the empc of each device
        rack_empc = self.get_rack_empc()
        indoor_aircon_empc, outdoor_aircon_empc, ceiling_light_empc, month, year = self.get_other_empc()

        # Extract the "Device Name", "Estimated Power Consumption" and "Plant Type" columns
        result_df = rack_empc[['Device Name', 'Estimated Power Consumption', 'Plant Type']]

        # Create a copy of the dataframe
        result_df = result_df.copy()

        # Split the 'Device Name' based on whitespace and join the first two elements
        result_df.loc[:, 'Consumer'] = result_df['Device Name'].str.split().str[:2].str.join(' ')

        # Group by 'Consumer' and 'Plant Type', and sum the 'Estimated Power Consumption' for each group
        result_df = result_df.groupby(['Consumer', 'Plant Type'], as_index=False)['Estimated Power Consumption'].sum()

        # Modify the copied dataframe
        result_df.loc[:, 'Power Consumption (kWh)'] = (result_df['Estimated Power Consumption'] / 1000).round(2)
        result_df.loc[:, 'Cost ($)'] = (result_df['Power Consumption (kWh)'] * ELECTRICITY_RATE).round(2)

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

        # Create a dictionary to store the other devices' data (consumer, epc in kWh and cost)
        other_device_data = {'Consumer': ['Indoor Aircon Unit 1', 'Indoor Aircon Unit 2', 'Outdoor Aircon Unit 1', 'Ceiling Lights'],
                            'Power Consumption (kWh)': [indoor_aircon_epc_kwh, indoor_aircon_epc_kwh, outdoor_aircon_epc_kwh, ceiling_light_epc_kwh],
                            'Cost ($)': [indoor_aircon_cost, indoor_aircon_cost, outdoor_aircon_cost, ceiling_light_cost]}
        
        # Make it into a dataframe
        other_device_df = pd.DataFrame(other_device_data)

        # Combine the 2 dataframes together 
        result_df = pd.concat([result_df, other_device_df], ignore_index=True)

        # Plotting Cost
        self.plot_bar_chart(result_df, 'Cost ($)', f'Predicted Cost ($) Of Each Consumer For {month} {year}', 'Predicted Monthly Cost.png')

        # Plotting Power Consumption
        self.plot_bar_chart(result_df, 'Power Consumption (kWh)', f'Predicted Power Consumption (kWh) Of Each Consumer For {month} {year}', 'Predicted Monthly Power Consumption.png')

        # Export the result_df as a csv
        result_df.to_csv(EMC_CSV, index=False)
        print('monthly_estimated_cost.csv created')

    ''' plot_bar_chart function is used to display the dataframe as a bar chart'''
    def plot_bar_chart(self, df, y_col, title, file_name):

        # Create a new column with the label
        df['Label'] = df['Consumer']

        # Filter out rows with NaN in 'Plant Type' and replace with empty string
        # df['Plant Type'] = df['Plant Type'].fillna('')
        # df['Label'] = df.apply(lambda row: f"{row['Consumer']} ({row['Plant Type']})" if row['Plant Type'] else row['Consumer'], axis=1)
        
        # Plotting chart with fixed size and aspect ratio
        plt.figure(figsize=(11, 6))
        bars = plt.bar(range(len(df)), df[y_col])
        plt.ylabel(y_col)
        plt.title(title)

        # Label the x axis ticks as numbers instead (prevent overcrowding the x axis)
        plt.xticks(range(len(df)), range(1, len(df) + 1))

        # Set the y-axis to logarithmic scale (makes the chart look more compact)
        plt.yscale('log')

        # Hide the y-axis tick labels
        plt.gca().set_yticklabels([])

        # Add the actual values on each bar
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, '%.2f' % height,
                    ha='center', va='bottom', fontsize=8)
            
        # Create the legend on the top right-hand side of the chart
        legend_labels = [f"{i+1}: {label}" for i, label in enumerate(df['Label'])]
        plt.legend(bars, legend_labels, loc='center left', bbox_to_anchor=(0, 0.77), fontsize=7)

        # Calculate and add the total of all the bar values
        total = round(df[y_col].sum(), 2)

        # Set the y-coordinate for the total text to the right of the entire bar graph
        right_margin = 0.25  # Adjust this value to fine-tune the position of the text
        plt.text(len(df) + right_margin, max(df[y_col]), f"Total Monthly {y_col}:\n{total}",
                ha='left', va='center', fontsize=9, bbox=dict(facecolor='white', edgecolor='black'))
        
        plt.subplots_adjust(right=0.7)  # Increase right margin to make space for legend and text

        # Save the plot as an image
        plt.savefig(os.path.join(OUTPUT_PNG_PATH,file_name))

        # Show the plot
        plt.show()

class DailyPowerCalculator():
    def __init__(self):
        pass
    
    ''' get_rack_monthly_edpc function is used to get the estimated daily power 
        consumption (edpc) of each device for each rack for the entire month'''
    def get_rack_monthly_edpc(self):
        # read the csv file
        predictions_df = pd.read_csv(PREDICTIONS_CSV)
        rack_df = pd.read_csv(RACK_EMPC_CSV)

        # rename the column to estimated power consumption (epc)
        predictions_df = predictions_df.rename(columns={'Prediction': 'Estimated Power Consumption'})

        # Get a list of unique "Device Name" from rack_df
        unique_device_names = rack_df['Device Name'].unique()

        # Get the number of days so that we can create the same amount of new rows for the other devices not in predictions_df
        days_in_month = predictions_df['Day of Month'].max()

        # Get the month so that we can set the values in the 'Month' column for new rows
        month = predictions_df['Month'].values[0]

        # Create an empty list to hold the new rows
        new_rows = []

        # Iterate over each unique "Device Name"
        for device_name in unique_device_names:
            # Check if the "Device Name" is not in predictions_df
            if device_name not in predictions_df['Device Name'].values:
                # Get the rows with the same "Device Name" in rack_df
                rows_for_device = rack_df[rack_df['Device Name'] == device_name]
                # Iterate over each day of the month
                for day in range(1, days_in_month + 1):
                    # Create a new row with the required columns and fill in the values
                    new_row = {
                        'Month': month,
                        'Day of Month': day,
                        'Estimated Power Consumption': rows_for_device['Estimated Power Consumption'].values[0],
                        'Device Name': device_name,
                        'Rack No': rows_for_device['Rack No'].values[0],
                        'Plant Type': rows_for_device['Plant Type'].values[0],
                        'Growth': rows_for_device['Growth'].values[0],
                    }
                    # Append the new row to the list of new rows
                    new_rows.append(new_row)

        # Create a new dataframe with the new rows
        new_rows_df = pd.DataFrame(new_rows)

        # Concatenate the original predictions_df and the new_rows_df to get the final dataframe
        combined_df = pd.concat([predictions_df, new_rows_df], ignore_index=True)

        # Merge the rack_df with combined_df based on 'Device Name', 'Rack No', 'Plant Type'
        combined_df = combined_df.merge(rack_df[['Device Name', 'Rack No', 'Plant Type', 'Growth']], on='Device Name', how='left')

        # Drop the original 'Rack No', 'Plant Type' and 'Growth' columns (if they exist) to avoid conflicts
        combined_df = combined_df.drop(columns=['Rack No_x', 'Plant Type_x', 'Growth_x'], errors='ignore')

        # Rename the merged 'Rack No', 'Plant Type' and 'Growth' columns to 'Plant Type' and 'Growth', respectively
        combined_df = combined_df.rename(columns={'Rack No_y': 'Rack No', 'Plant Type_y': 'Plant Type', 'Growth_y': 'Growth'})

        # Iterate over each row in the DataFrame
        for index, row in combined_df.iterrows():
            # find rows with 0 epc
            if row['Estimated Power Consumption'] == 0:
                similar_device_type = row['Device Name'].split(' ')[-1]
                # first find similar row based on their plant type and device type
                similar_rows = combined_df[(combined_df['Rack No'] != row['Rack No']) &
                                        (combined_df['Plant Type'] == row['Plant Type']) &
                                        (combined_df['Day of Month'] == row['Day of Month']) &
                                        (combined_df['Device Name'].str.endswith(similar_device_type))]
                # if no similar rows, then find one based on their growth
                if similar_rows.empty:
                    similar_rows = combined_df[(combined_df['Rack No'] != row['Rack No']) &
                                            (combined_df['Growth'] == row['Growth']) &
                                            (combined_df['Day of Month'] == row['Day of Month']) &
                                            (combined_df['Device Name'].str.endswith(similar_device_type))]
                # if have similar rows, then set the row's epc with the same value as the similar_row's epc
                if not similar_rows.empty:
                    similar_row = similar_rows.iloc[0]
                    combined_df.at[index, 'Estimated Power Consumption'] = similar_row['Estimated Power Consumption']

        # Group by 'Month' and 'Day of Month' and sum up the 'Estimated Power Consumption'
        combined_df = combined_df.groupby(['Month', 'Day of Month'])['Estimated Power Consumption'].sum().reset_index()

        # Drop all columns except 'Month', 'Day of Month', and 'Estimated Power Consumption'
        combined_df = combined_df[['Month', 'Day of Month', 'Estimated Power Consumption']]

        return combined_df

    ''' get_other_edpc function is used to get the edpc of other devices in the
        container for the entire month'''
    def get_other_edpc(self):
        # edpc based on each device's specifications, operating hours and number of days

        # Indoor aircon unit
        indoor_aircon_edpc = INDOOR_AIRCON_FAN * 24
        # Outdoor aircon unit
        outdoor_aircon_edpc = (((OUTDOOR_AIRCON_COOLING_MAX + OUTDOOR_AIRCON_COOLING_MIN)/2) + OUTDOOR_AIRCON_COMPRESSOR_NORM + OUTDOOR_AIRCON_FAN) * 24
        # to be updated once more data for ambient comes in
        ceiling_light_edpc = CEILING_LIGHT_POWER * NO_OF_LIGHTS * 1

        return indoor_aircon_edpc, outdoor_aircon_edpc, ceiling_light_edpc

    ''' get_total_edpc function is used to get all the edpc of racks and other
        devices and exports the result as a csv'''
    def get_total_edpc(self):
        # Call functions to get racks' and other devices' edpc
        indoor_aricon_edpc, outdoor_aircon_edpc, ceiling_lights_edpc = self.get_other_edpc()
        daily_epc_df = self.get_rack_monthly_edpc()

        # Iterate over each row in the dataframe
        for index, row in daily_epc_df.iterrows():
            # Add the values of the additional columns to the 'Estimated Power Consumption' for the current row
            daily_epc_df.at[index, 'Estimated Power Consumption'] += indoor_aricon_edpc + outdoor_aircon_edpc + ceiling_lights_edpc

        # Divide the 'Estimated Power Consumption' by 1000 to get the 'Estimated Daily Power Consumption (kWh)'
        daily_epc_df['Estimated Power Consumption'] /= 1000

        # Round the 'Estimated Power Consumption' column to 2 significant figures
        daily_epc_df['Estimated Power Consumption'] = daily_epc_df['Estimated Power Consumption'].round(2)

        # Rename the column to 'Estimated Daily Power Consumption (kWh)'
        daily_epc_df = daily_epc_df.rename(columns={'Estimated Power Consumption': 'Estimated Daily Power Consumption (kWh)'})

        # Exports the dataframe as a csv
        daily_epc_df.to_csv(EDPC_CSV, index=False)

        print('daily_estimated_pc.csv created')

# Main program
if __name__ == "__main__":
    # Check if csv files exist
    if os.path.isfile(PREDICTIONS_CSV) & os.path.isfile(RACK_EMPC_CSV):
        cost_calculator = MonthlyCostCalculator()
        daily_power_calculator = DailyPowerCalculator()

        cost_calculator.calculate_cost()
        daily_power_calculator.get_total_edpc()
    else:
        print("CSV files don't exist")
