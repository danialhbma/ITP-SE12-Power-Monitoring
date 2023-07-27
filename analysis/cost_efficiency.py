import os
import pandas as pd
from collections import defaultdict
from pytz import timezone

# Constants
TIMEZONE = timezone('Etc/GMT+8')
PC_PATH = "data/Power Consumption.csv"
TEMP_PATH = "data/WeatherAPI.csv"

# Refer to https://www.senokoenergy.com/households/price-plans
POWER_COST_PER_KWH = 0.2898
POWER_READ_INTERVAL = 1 # in hours

# Function that returns cost efficient season (above 31, 27 to 31, below 27) for the previous month
def get_cost_efficient_season():
    high_power = 0
    average_power = 0
    low_power = 0

    # Track number of hours for respective data (to find average for better comparison)
    high_hours = 0
    average_hours = 0
    low_hours = 0

    for time, temp, type in temp_data.values:
        # Skip all rows not temperature readings
        if type != "temperature":
            continue

        power_data = pc_data_dict.get(time, 0)
        if power_data != 0:
            if temp > 30:
                high_power += power_data
                high_hours += 1
            elif 25 <= temp <= 30:
                average_power += power_data
                average_hours += 1
            else:
                low_power += power_data
                low_hours += 1

    high_power /= high_hours
    average_power /= average_hours
    low_power /= low_hours

    print("Average power per hour consumed > 31 degree celsius: %.2f W/h" % high_power)
    print("Average power per hour consumed > 27 and > 31 celsius: %.2f W/h" % average_power)
    print("Average power per hour consumed < 27 degree celsius: %.2f W/h" % low_power)

    best_season = min(high_power, average_power, low_power)
    if best_season == high_power:
        print("Most cost efficient period is when temperature goes above 31 degree celsius.")
    elif best_season == average_power:
        print("Most cost efficient season is when temperature is between 27 and 31 degree celsius.")
    elif best_season == low_power:
        print("Most cost efficient season is when temperature falls above 27 degree celsius.")

# Function that returns cost efficient period (day/night) for the previous month
def get_cost_efficient_period():
    day_power = 0
    night_power = 0

    for time in pc_data_dict:
        convertedTime = pd.to_datetime(time).tz_convert(TIMEZONE)
        if convertedTime.time() >= pd.to_datetime('07:00:00').time() and convertedTime.time() <= pd.to_datetime("19:00:00").time():
            day_power += pc_data_dict[time] * POWER_READ_INTERVAL / 1000
        else:
            night_power += pc_data_dict[time] * POWER_READ_INTERVAL / 1000

    day_amount = day_power * POWER_COST_PER_KWH
    night_amount = night_power * POWER_COST_PER_KWH
    
    print("Amount spent during the day: $%.2f" % day_amount)
    print("Amount spent during the night: $%.2f" % night_amount)

    best_period = min(day_amount, night_amount)
    if best_period == day_amount:
        print("Most cost efficient period is from 0700-1900.")
    elif best_period == night_amount:
        print("Most cost efficient period is from 1900-0700.")

# Check if csv files exists
if os.path.isfile(PC_PATH) and os.path.isfile(TEMP_PATH):
    pc_data = pd.read_csv(PC_PATH, usecols=[0, 1])
    temp_data = pd.read_csv(TEMP_PATH, usecols=[0, 1, 2])

    # Create a defaultdict to store pc_data values based on time (and account for duplicates)
    pc_data_dict = defaultdict(float)
    for time, power in pc_data.values:
        pc_data_dict[time] += power

    # Run analysis codes
    get_cost_efficient_period()
    get_cost_efficient_season()
else:
    print("File does not exist.")
