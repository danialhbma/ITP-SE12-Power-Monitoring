import os
import pandas as pd
from collections import defaultdict
import calendar
from datetime import datetime

PC_PATH = "analysis/data/Power Consumption.csv"

# Senoko's power cost - Refer to https://www.senokoenergy.com/households/price-plans
POWER_COST_PER_KWH = 0.2898

RACKS = ["Rack_1", "Rack_2" ] # racks observed
POWER_READ_INTERVAL = 1  # in hours
WHOLE_DAY = 24 # in hours

# rough baseline for racklights on/off 
BASELINE_MIN_PURPLE_LED_ON = 390
BASELINE_MAX_PURPLE_LED_ON = 395
BASELINE_MIN_PURPLE_LED_OFF = 0.80
BASELINE_MAX_PURPLE_LED_OFF = 0.95

BASELINE_MIN_WHITE_LED_ON = 360
BASELINE_MAX_WHITE_LED_ON = 365
BASELINE_MIN_WHITE_LED_OFF = 0.90
BASELINE_MAX_WHITE_LED_OFF = 1.015

BASELINE_MIN_WATER = 18.5
BASELINE_MAX_WATER = 23.5

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

# basic function that calculates power kWh based on wattage, days ran and hours ran
def calculate_power_from_watts(appliance_wattage, days_ran, hours_ran, num_of_racks):
    return round((appliance_wattage * days_ran * hours_ran * num_of_racks) / 1000, 2)

# function that returns mean watts measured for each rack light and water pump
def get_mean_watt_measured(pc_data, racks = RACKS):
    light_mean_dict = {}
    purple_led_on_list = []
    purple_led_off_list = []
    white_led_on_list = []
    white_led_off_list = []
    water_list = []
    
    # set datetime as index
    pc_data.set_index('_time', inplace=True)
    
    # filter on/off values based led colour
    for rack in racks:
        # take all water values since water pumps are always on
        water_list.append(pc_data[(pc_data['_value'] >= BASELINE_MIN_WATER) & (pc_data['_value'] <= BASELINE_MAX_WATER) & (pc_data['_measurement'] == rack + '_Water')])
        
        # filter rack light on/off values based on recorded baseline vals for each led colour
        if rack.endswith('1'):  
            rack_light_on = pc_data[(pc_data['_value'] >= BASELINE_MIN_PURPLE_LED_ON) & (pc_data['_value'] <= BASELINE_MAX_PURPLE_LED_ON) & (pc_data['_measurement'] == rack + '_Light')]
            rack_light_off = pc_data[(pc_data['_value'] >= BASELINE_MIN_PURPLE_LED_OFF) & (pc_data['_value'] <= BASELINE_MAX_PURPLE_LED_OFF) & (pc_data['_measurement'] == rack + '_Light')]
            purple_led_on_list.append(rack_light_on)
            purple_led_off_list.append(rack_light_off)
            
        else:
            rack_light_on = pc_data[(pc_data['_value'] >= BASELINE_MIN_WHITE_LED_ON) & (pc_data['_value'] <= BASELINE_MAX_WHITE_LED_ON) & (pc_data['_measurement'] == rack + '_Light')]
            rack_light_off = pc_data[(pc_data['_value'] >= BASELINE_MIN_WHITE_LED_OFF) & (pc_data['_value'] <= BASELINE_MAX_WHITE_LED_OFF) & (pc_data['_measurement'] == rack + '_Light')]
            white_led_on_list.append(rack_light_on)
            white_led_off_list.append(rack_light_off)    
    
    # concat all dataframes
    purple_led_on = pd.concat(purple_led_on_list)
    purple_led_off = pd.concat(purple_led_off_list)
    white_led_on = pd.concat(white_led_on_list)
    white_led_off = pd.concat(white_led_off_list)
    water = pd.concat(water_list)    
        
    # Calculate the mean for the each rack and on/off state
    light_mean_dict['Purple_LED_On'] = round(purple_led_on['_value'].mean(), 2)
    light_mean_dict['Purple_LED_Off'] = round(purple_led_off['_value'].mean(), 2)
    light_mean_dict['White_LED_On'] = round(white_led_on['_value'].mean(), 2)
    light_mean_dict['White_LED_Off'] = round(white_led_off['_value'].mean(), 2)
    water_pump_wattage = round(water['_value'].mean(), 2)
        
    return light_mean_dict, water_pump_wattage

# returns the power consumption of water pumps in kWh
def get_water_power_consumption(water_pump_wattage,
                                days_ran,
                                hours_ran = WATER_PUMP_RUNTIME,
                                total_racks = NUM_OF_PURPLE_LED_RACKS + NUM_OF_WHITE_LED_RACKS):
    
    water_power = calculate_power_from_watts(water_pump_wattage, days_ran, hours_ran, total_racks)
    return water_power

# returns power consumption of each rack light based on its usage in kWh
# details: 0 for simple (returns purple led and white led power) and 1 for detailed (returns led power based on colour and state)
def get_racklight_power_consumption(details,
                                    light_mean_dict,
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
    purple_led_on_power = calculate_power_from_watts(purple_led_on_mean, days_ran, purple_led_hours_ran, purple_led_racks)
    purple_led_off_power = calculate_power_from_watts(purple_led_off_mean, days_ran, (whole_day - purple_led_hours_ran), purple_led_racks)
    
    white_led_on_power = calculate_power_from_watts(white_led_on_mean, days_ran, white_led_hours_ran, white_led_racks)
    white_led_off_power = calculate_power_from_watts(white_led_off_mean, days_ran, (whole_day - white_led_hours_ran), white_led_racks)
    
    # if simple data needed, return the total power consumption of each led
    if details == 0:
        purple_led_power = purple_led_on_power + purple_led_off_power
        white_led_power = white_led_on_power + white_led_off_power
        return purple_led_power, white_led_power
    
    # if detailed data needed, return power consumption of each led based on its colour and on/off state
    else:
        return purple_led_on_power, purple_led_off_power, white_led_on_power, white_led_off_power

# returns power consumption of aircon in kWh
def get_aircon_power_consumption(days_ran,
                                num_of_hours_ran = WHOLE_DAY,
                                num_of_units = NUM_OF_AIRCON_UNITS,
                                total_watts = INDOOR_FAN + COOLING + COMPRESSOR + OUTDOOR_FAN):
    return round((total_watts * days_ran * num_of_hours_ran / 1000) * num_of_units, 2)

# returns cost of running appliance based on the given power (in kwh) used and cost per kwh
def calculate_cost(power_used, cost_per_kwh = POWER_COST_PER_KWH):
    return round(power_used  * cost_per_kwh, 2)
    
