import os
import pandas as pd
from collections import defaultdict
from pytz import timezone

# Constants
TIMEZONE = timezone('Etc/GMT+8')
# PATHS TO BE UPDATED
PC_PATH = "InfluxDB/data/Power Consumption_20230716172100.csv"
TEMP_PATH = "InfluxDB/data/WeatherAPI_20230716172054.csv"
KW_MULTIPLIER = 60 * 60 / 1000 # assuming data consistency for the whole hour, and to convert to kilowatts
POWER_COST_DAY = 0.03
POWER_COST_NIGHT = 0.05

# Check if csv files exists
if os.path.isfile(PC_PATH) and os.path.isfile(TEMP_PATH):
    pc_data = pd.read_csv(PC_PATH, usecols=[0, 1])
    temp_data = pd.read_csv(TEMP_PATH, usecols=[0, 1])

    # Create a defaultdict to store pc_data values based on time (and account for duplicates)
    pc_data_dict = defaultdict(float)
    for time, power in pc_data.values:
        pc_data_dict[time] += power
else:
    print("File does not exist.")

# Function that returns cost efficient season (above 31, 27 to 31, below 27) for the previous month
def get_cost_efficient_season():
    high_power = 0
    average_power = 0
    low_power = 0
    
    for time, temp in temp_data.values:
        if temp > 31:
            high_power += pc_data_dict.get(time, 0)
        elif 27 <= temp <= 31:
            average_power += pc_data_dict.get(time, 0)
        else:
            low_power += pc_data_dict.get(time, 0)

    high_power *= KW_MULTIPLIER
    average_power *= KW_MULTIPLIER
    low_power *= KW_MULTIPLIER

    print("Amount of power (abv 31 deg celsius): %.2fkW" % high_power)
    print("Amount of power (27-31 deg celsius): %.2fkW" % average_power)
    print("Amount of power (bel 27 deg celsius): %.2fkW" % low_power)

# Function that returns cost efficient period (day/night) for the previous month
def get_cost_efficient_period():
    day_power = 0
    night_power = 0

    for time in pc_data_dict:
        theTime = pd.to_datetime(time)
        theTime = theTime.tz_convert(TIMEZONE)

        if theTime.time() >= pd.to_datetime('07:00:00').time() and theTime.time() <= pd.to_datetime("19:00:00").time():
            day_power += pc_data_dict[time]
        else:
            night_power += pc_data_dict[time]

    day_power *= KW_MULTIPLIER
    night_power *= KW_MULTIPLIER
    
    print("Amount of power during the day: %.2fkW" % day_power)
    print("Amount of power during the night: %.2fkW" % night_power)

# Run analysis codes
get_cost_efficient_period()
get_cost_efficient_season()
