import os
import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# constants
PC_PATH = "analysis/data/Power Consumption.csv"
OUTPUT_ANALYSIS_IMG_PATH = "analysis/results/"
POWER_READ_INTERVAL = 1  # in hours
WHOLE_DAY = 24 # in hours

# indoor: Therm-Aire STA-024SPWM
INDOOR_FAN = 120
NUM_OF_INDOOR_UNITS = 2

# outdoor: Therm-Aire STA5-048SPMM
OUTDOOR_COOLING_MIN = 855
OUTDOOR_COOLING_MAX = 4795
OUTDOOR_COMPRESSOR_NORM = 2820
OUTDOOR_COMPRESSOR_MAX = 3040
OUTDOOR_FAN = 85

# racks observed and total number of racks currently in use in the container
RACKS = ["Rack_1", "Rack_2", "Rack_3"]
NUM_OF_WHITE_LED_RACKS = 6
NUM_OF_PURPLE_LED_RACKS = 3

# function that gets power consumption of all water pumps used rounded to 2dp
def get_water_power_consumption(pc_data_dict, total_racks_used):
    water_power_consumption = 0
    
    # calculate the total power consumption of water pumps from observed data
    for rack in RACKS:
        water_power_consumption += (pc_data_dict[rack + "_Water"]) * POWER_READ_INTERVAL / 1000

    # use the observed data to estimate power consumption of all racks in use
    return round(water_power_consumption / len(RACKS) * total_racks_used, 2)
    
# function that gets power consumption of all rack LED lights used
# output: power consumption of white led lights and purple led lights, rounded to 2dps
def get_racklight_power_consumption(pc_data_dict, num_of_purple_led_racks, num_of_white_led_racks):
    purple_led_power_consumption = 0
    white_led_power_consumption = 0
    num_purple_racks_observed = 0
    
    # calculate the total power consumption of lights from observed data
    # rack 1 is using purple LED, racks 2 and 3 is using white LED
    for rack in RACKS:
        # filter by racks observed
        if rack.endswith('1'): 
            purple_led_power_consumption += (pc_data_dict[rack + "_Light"]) * POWER_READ_INTERVAL / 1000
            num_purple_racks_observed += 1
        else:
            white_led_power_consumption += (pc_data_dict[rack + "_Light"]) * POWER_READ_INTERVAL / 1000
    
    # use the observed data to estimate power consumption of all racks in use
    purple_led_power_consumption = round(purple_led_power_consumption / num_purple_racks_observed * NUM_OF_PURPLE_LED_RACKS, 2)
    white_led_power_consumption = round(white_led_power_consumption / (len(RACKS) - num_purple_racks_observed) * NUM_OF_WHITE_LED_RACKS, 2)
    
    return purple_led_power_consumption, white_led_power_consumption

# function that calculates the power consumption of the air conditioner at maximum cooling capacity
# assumption: aircon runs for 24 hours a day for the specified number of days
def get_max_aircon_power(number_of_days):
    indoor = INDOOR_FAN * NUM_OF_INDOOR_UNITS
    outdoor = OUTDOOR_COOLING_MAX + OUTDOOR_COMPRESSOR_MAX + OUTDOOR_FAN
    return round((indoor + outdoor) * number_of_days * WHOLE_DAY / 1000 ,2)

# function that calculates the average power consumption of the air conditioner at normal cooling capacity
# assumption: aircon runs for 24 hours a day for the specified number of days
def get_avg_aircon_power(number_of_days):
    avg_outdoor_cooling = (OUTDOOR_COOLING_MIN + OUTDOOR_COOLING_MAX)/2
    indoor = INDOOR_FAN * NUM_OF_INDOOR_UNITS
    outdoor = avg_outdoor_cooling + OUTDOOR_COMPRESSOR_NORM + OUTDOOR_FAN
    return round((indoor + outdoor) * number_of_days * WHOLE_DAY / 1000 ,2)

# function that returns the number of days the data was collected over
def get_days_observed(pc_data):
    # get datetime col in dataframe
    pc_data.iloc[:, 0] = pd.to_datetime(pc_data.iloc[:, 0])
    
    # get date range 
    first_date = pc_data.iloc[:, 0].min()
    last_date = pc_data.iloc[:, 0].max()
    number_of_days = (last_date - first_date).days + 1

    return number_of_days

# function that generates a pie chart using the estimated power consumption and saves as png file
def generate_pie_chart(estimated_power_dict, filename): 
    # get pie chart data and labels from the dictionary
    data = np.array(list(estimated_power_dict.values()))
    labels = list(estimated_power_dict.keys())

    plt.figure(figsize=(12, 7))
    plt.title(filename, pad=40)
    
    plt.pie(data,
            labels = labels,
            autopct = lambda x: f'{x:.2f}%\n({(x/100)*sum(data):.2f} kWh)',
            pctdistance = 1.2,
            labeldistance=1.4,
            textprops={'horizontalalignment': 'center',
                       'verticalalignment':'top'})
    
    plt.legend(loc='lower right',
               bbox_to_anchor=(1, 0),
               title='Variables')
    
    plt.axis('equal')
    plt.subplots_adjust(top=1, right=0.8)  # increase margins to create more space for title and legend
    plt.tight_layout()  # automatically adjust the layout to fit the content
    
    # save the pie chart as image
    plt.savefig(OUTPUT_ANALYSIS_IMG_PATH + filename, bbox_inches='tight')

# check if csv files exists
if os.path.isfile(PC_PATH):
    pc_data = pd.read_csv(PC_PATH, usecols=[0, 1, 3])
    number_of_days = get_days_observed(pc_data)
    
    # drop datetime col from dataframe
    pc_data = pc_data.drop(pc_data.columns[0], axis=1)
    
    # create a defaultdict to store pc_data values based on time (and account for duplicates)
    pc_data_dict = defaultdict(float)
    for power, reading in pc_data.values:
        pc_data_dict[reading] += power
    
    # store estimdated power consumption in dictionary
    estimated_pc_dict = {}
    purple_racklight, white_racklight = get_racklight_power_consumption(pc_data_dict, NUM_OF_PURPLE_LED_RACKS, NUM_OF_WHITE_LED_RACKS)
    estimated_pc_dict['Water'] = get_water_power_consumption(pc_data_dict, NUM_OF_PURPLE_LED_RACKS + NUM_OF_WHITE_LED_RACKS)
    estimated_pc_dict['Purple LED Rack Lights'] = purple_racklight
    estimated_pc_dict['White LED Rack Lights'] = white_racklight
    estimated_pc_dict['Aircon (Average Capacity)'] = get_avg_aircon_power(number_of_days)
    
    # generate charts for both average and max capacity
    generate_pie_chart(estimated_pc_dict, 'Variables that Affect Monthly Power Consumption - Average Capacity')
    
    estimated_pc_dict.pop("Aircon (Average Capacity)", None)
    estimated_pc_dict['Aircon (Max Capacity)'] = get_max_aircon_power(number_of_days)
    generate_pie_chart(estimated_pc_dict, 'Variables that Affect Monthly Power Consumption - Max Capacity')

else:
    print("File does not exist.")
