import os
import pandas as pd
from collections import defaultdict

PC_PATH = "./data/Power Consumption.csv"

RACKS = ["Rack_1", "Rack_2", "Rack_3"] # racks observed
POWER_READ_INTERVAL = 1  # in hours
WHOLE_DAY = 24 # in hours

# indoor aircon unit: Therm-Aire STA-024SPWM
INDOOR_FAN = 120
NUM_OF_INDOOR_UNITS = 2

# outdoor aircon unit: Therm-Aire STA5-048SPMM
OUTDOOR_COOLING_MIN = 855
OUTDOOR_COOLING_MAX = 4795
OUTDOOR_COMPRESSOR_NORM = 2820
OUTDOOR_COMPRESSOR_MAX = 3040
OUTDOOR_FAN = 85

# total number of racks currently in use in the container
NUM_OF_WHITE_LED_RACKS = 6
NUM_OF_PURPLE_LED_RACKS = 3

def get_pc_data(pc_path=PC_PATH):    
    if os.path.isfile(pc_path):
        pc_data = pd.read_csv(pc_path, usecols=[0, 1, 3])
        number_of_days_observed = get_days_observed(pc_data)
        # drop datetime col from dataframe
        pc_data = pc_data.drop(pc_data.columns[0], axis=1)
        
        # create a defaultdict to store pc_data values based on time (and account for duplicates)
        pc_data_dict = defaultdict(float)
        for power, reading in pc_data.values:
            pc_data_dict[reading] += power
            
        return pc_data_dict, number_of_days_observed
    else:
        return None
    
# function that returns the number of days the data was collected over
def get_days_observed(pc_data):
    # get datetime col in dataframe
    pc_data.iloc[:, 0] = pd.to_datetime(pc_data.iloc[:, 0])
    
    # get date range 
    first_date = pc_data.iloc[:, 0].min()
    last_date = pc_data.iloc[:, 0].max()
    number_of_days_observed = (last_date - first_date).days + 1

    return number_of_days_observed

# function that gets power consumption of all water pumps used rounded to 2dp
def get_water_power_consumption(pc_data_dict,
                                total_racks_used = NUM_OF_PURPLE_LED_RACKS + NUM_OF_WHITE_LED_RACKS):
    water_power_consumption = 0
    
    # calculate the total power consumption of water pumps from observed data
    for rack in RACKS:
        water_power_consumption += (pc_data_dict[rack + "_Water"]) * POWER_READ_INTERVAL / 1000

    # use the observed data to estimate power consumption of all racks in use
    return round(water_power_consumption / len(RACKS) * total_racks_used, 2)
    
# function that gets power consumption of all rack LED lights used
# output: power consumption of white led lights and purple led lights, rounded to 2dps
def get_racklight_power_consumption(pc_data_dict,
                                    num_of_purple_led_racks = NUM_OF_PURPLE_LED_RACKS,
                                    num_of_white_led_racks = NUM_OF_WHITE_LED_RACKS):
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
    purple_led_power_consumption = round(purple_led_power_consumption / num_purple_racks_observed * num_of_purple_led_racks, 2)
    white_led_power_consumption = round(white_led_power_consumption / (len(RACKS) - num_purple_racks_observed) * num_of_white_led_racks, 2)
    
    return purple_led_power_consumption, white_led_power_consumption

# function that calculates the power consumption of the air conditioner at maximum cooling capacity
# assumption: aircon runs for 24 hours a day for the specified number of days
def get_max_aircon_power(number_of_days,
                         number_of_hours_ran = WHOLE_DAY):
    indoor = INDOOR_FAN * NUM_OF_INDOOR_UNITS
    outdoor = OUTDOOR_COOLING_MAX + OUTDOOR_COMPRESSOR_MAX + OUTDOOR_FAN
    return round((indoor + outdoor) * number_of_days * number_of_hours_ran / 1000, 2)

# function that calculates the average power consumption of the air conditioner at normal cooling capacity
# assumption: aircon runs for 24 hours a day for the specified number of days
def get_avg_aircon_power(number_of_days,
                         number_of_hours_ran = WHOLE_DAY):
    avg_outdoor_cooling = (OUTDOOR_COOLING_MIN + OUTDOOR_COOLING_MAX)/2
    indoor = INDOOR_FAN * NUM_OF_INDOOR_UNITS
    outdoor = avg_outdoor_cooling + OUTDOOR_COMPRESSOR_NORM + OUTDOOR_FAN
    return round((indoor + outdoor) * number_of_days * number_of_hours_ran / 1000, 2)
