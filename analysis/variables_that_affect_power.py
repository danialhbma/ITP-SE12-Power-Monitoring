import os
import pandas as pd
from collections import defaultdict

# constants
PC_PATH = "analysis/data/Power Consumption.csv"
POWER_READ_INTERVAL = 1 # in hours

# indoor: Therm-Aire STA-024SPWM
INDOOR_FAN = 120
NUM_OF_INDOOR_UNITS = 2

# outdoor: Therm-Aire STA5-048SPMM
OUTDOOR_COOLING_MIN = 855
OUTDOOR_COOLING_MAX = 4795
OUTDOOR_COMPRESSOR_NORM = 2820
OUTDOOR_COMPRESSOR_MAX = 3040
OUTDOOR_FAN = 85

# racks
RACKS = ["Rack_1", "Rack_2", "Rack_3"]

def get_light_water_power(pc_data_dict):
    light = 0
    water = 0
    
    # calculate the total power consumption of lights and water pumps from the db data
    for rack in RACKS:
        light += (pc_data_dict[rack + "_Light"]) * POWER_READ_INTERVAL / 1000
        water += (pc_data_dict[rack + "_Water"]) * POWER_READ_INTERVAL / 1000

    return light, water

# calculate the power consumption of the air conditioner at maximum cooling capacity
def get_max_aircon_power():
    return ((INDOOR_FAN * NUM_OF_INDOOR_UNITS) + OUTDOOR_COOLING_MAX + OUTDOOR_COMPRESSOR_MAX + OUTDOOR_FAN) * POWER_READ_INTERVAL / 1000

# calculate the average power consumption of the air conditioner at normal cooling capacity
def get_avg_aircon_power():
    avg_outdoor_cooling = (OUTDOOR_COOLING_MIN + OUTDOOR_COOLING_MAX)/2
    return ((INDOOR_FAN * NUM_OF_INDOOR_UNITS)+ avg_outdoor_cooling + OUTDOOR_COMPRESSOR_NORM + OUTDOOR_FAN) * POWER_READ_INTERVAL / 1000

# check if csv files exists
if os.path.isfile(PC_PATH):
    pc_data = pd.read_csv(PC_PATH, usecols=[1, 3])

    # create a defaultdict to store pc_data values based on time (and account for duplicates)
    pc_data_dict = defaultdict(float)
    
    for power, reading in pc_data.values:
        pc_data_dict[reading] += power

    light, water = get_light_water_power(pc_data_dict)
    avg_aircon = get_avg_aircon_power()
    max_aircon = get_max_aircon_power()
    
    avg_power = light + water + avg_aircon
    max_power = light + water + max_aircon
    
    print("Rack lights power consumption per hour: %.2fkWh" % light)
    print("Water pumps power consumption per hour: %.2fkWh" % water)
    
    print("")
    print("Normal aircon power consumption per hour: %.2fkWh" % avg_aircon)
    print("Average power consumption per hour: %.2fkWh" % avg_power)
    print("Max aircon power consumption per hour: %.2fkWh" % max_aircon)
    print("Max power consumption per hour: %.2fkWh" % max_power)
    
    print("")
    print("Rack lights contribute {:.2%} to avg power consumption".format(light/avg_power))
    print("Water pumps contribute {:.2%} to avg power consumption".format(water/avg_power))
    print("Aircon contribute {:.2%} to avg power consumption".format(avg_aircon/avg_power))
    
    print("")
    print("Rack lights contribute {:.2%} to max power consumption".format(light/max_power))
    print("Water pumps contribute {:.2%} to max power consumption".format(water/max_power))
    print("Aircon contribute {:.2%} to max power consumption".format(max_aircon/max_power))
    
    
else:
    print("File does not exist.")