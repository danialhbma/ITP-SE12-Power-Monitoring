import os
import pandas as pd
from collections import defaultdict
from pytz import timezone
import calendar
from datetime import datetime

PC_PATH = "analysis/data/Power Consumption.csv"

TIMEZONE = timezone('Asia/Singapore')
RACKS = ["Rack_1", "Rack_2"] # racks observed
POWER_READ_INTERVAL = 1  # in hours
WHOLE_DAY = 24 # in hours

# rough baseline for racklights on/off 
BASELINE_RACKLIGHT_ON = 350
BASELINE_RACKLIGHT_OFF = 2

# aircon unit: Therm-Aire STA-024SPWM (single split)
INDOOR_FAN = 58
COOLING = 1230
COMPRESSOR = 1970
OUTDOOR_FAN = 58
NUM_OF_AIRCON_UNITS = 2

# total number of racks currently in use in the container
NUM_OF_WHITE_LED_RACKS = 6
NUM_OF_PURPLE_LED_RACKS = 3

# time that the rack water pumps and rack led lights are currently run for
WATER_PUMP_RUNTIME = 24
RACK_LIGHT_RUNTIME = 12

def get_pc_data(pc_path=PC_PATH):    
    if os.path.isfile(pc_path):
        pc_data = pd.read_csv(pc_path, usecols=['_time', '_value', '_measurement'])        
        return pc_data
    else:
        return None

# function that returns the number of days in current month
def get_days_in_month():
    current_year = datetime.now().year
    current_month = datetime.now().month
    return calendar.monthrange(current_year, current_month)[1]

# function that returns mean watts measured for each rack light and water pump
def get_mean_watt_measured(pc_data, racks = RACKS):
    # convert time to correct timezone and set as index
    pc_data['_time'] = pd.to_datetime(pc_data['_time'])
    pc_data['_time'] = pc_data['_time'].dt.tz_convert(TIMEZONE)
    pc_data.set_index('_time', inplace=True)
    
    light_mean_dict = {}
    water_sum = 0
    
    # filter on/off values based led colour
    for rack in racks:
        # filter rack light on/off values based on recorded baseline vals
        rack_light_on = pc_data[(pc_data['_value'] >= BASELINE_RACKLIGHT_ON) & (pc_data['_measurement'] == rack + '_Light')]
        rack_light_off = pc_data[(pc_data['_value'] <= BASELINE_RACKLIGHT_OFF) & (pc_data['_measurement'] == rack + '_Light')]
        
        # take all water values since water pumps are always on
        rack_water = pc_data[(pc_data['_measurement'] == rack + '_Water')]
        
        # Calculate the mean for the current rack and day/night
        rack_light_on_mean = round(rack_light_on['_value'].mean(), 2)
        rack_light_off_mean = round(rack_light_off['_value'].mean(), 2)
        water_sum += round(rack_water['_value'].mean(), 2)
        
        # store the mean values in the dictionary based on rack led colour
        if rack.endswith('1'):     
            light_mean_dict['Purple_LED_On'] = rack_light_on_mean
            light_mean_dict['Purple_LED_Off'] = rack_light_off_mean
        else:
            light_mean_dict['White_LED_On'] = rack_light_on_mean
            light_mean_dict['White_LED_Off'] = rack_light_off_mean
    
        # find mean of observed water pumps
        water_mean = water_sum / len(racks)
        
    return light_mean_dict, water_mean

# returns the power consumption of water pumps in kWh
def get_water_power_consumption(water_mean,
                                days_ran,
                                hours_ran = WATER_PUMP_RUNTIME,
                                total_racks = NUM_OF_PURPLE_LED_RACKS + NUM_OF_WHITE_LED_RACKS):
    
    water_power = round((water_mean  * days_ran * hours_ran * total_racks) / 1000, 2)
    return water_power

# returns power consumption of each rack light based on its usage in kWh
def get_racklight_power_consumption(light_mean_dict,
                                       days_ran,
                                       purple_led_hours_ran = RACK_LIGHT_RUNTIME,
                                       white_led_hours_ran = RACK_LIGHT_RUNTIME,
                                       purple_led_racks = NUM_OF_PURPLE_LED_RACKS,
                                       white_led_racks = NUM_OF_WHITE_LED_RACKS,
                                       whole_day = WHOLE_DAY):
    
    # get mean watt measured for both white and purple leds
    purple_led_on_mean = light_mean_dict['Purple_LED_On']
    white_led_on_mean = light_mean_dict['White_LED_On']
    purple_led_off_mean = light_mean_dict['Purple_LED_Off']
    white_led_off_mean = light_mean_dict['White_LED_Off']
    
    # find power consumption of each led running for the specified number of hours
    purple_led_on_power = round((purple_led_on_mean * days_ran * purple_led_hours_ran * purple_led_racks) / 1000, 2)
    purple_led_off_power = round((purple_led_off_mean * days_ran * (whole_day - purple_led_hours_ran) * purple_led_racks) / 1000, 2)
    
    white_led_on_power = round((white_led_on_mean * days_ran * white_led_hours_ran * white_led_racks) / 1000, 2)
    white_led_off_power = round((white_led_off_mean * days_ran * (whole_day - white_led_hours_ran)) * white_led_racks / 1000, 2)
    
    return purple_led_on_power, purple_led_off_power, white_led_on_power, white_led_off_power

# returns power consumption of aircon in kWh
def get_aircon_power_consumption(days_ran,
                                num_of_hours_ran = WHOLE_DAY,
                                num_of_units = NUM_OF_AIRCON_UNITS):
    total_watts = INDOOR_FAN + COOLING + COMPRESSOR + OUTDOOR_FAN
    return round((total_watts * days_ran * num_of_hours_ran / 1000) * num_of_units, 2)
