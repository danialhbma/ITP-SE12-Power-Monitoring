import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from calculate_power_consumption import *

# constants
OUTPUT_ANALYSIS_IMG_PATH = "analysis/results/"

# function that generates a pie chart using the estimated power consumption and saves as png file
def generate_pie_chart(estimated_power_dict, filename): 
    # get pie chart data and labels from the dictionary
    data = np.array(list(estimated_power_dict.values()))
    labels = list(estimated_power_dict.keys())

    plt.figure(figsize=(12, 7))
    plt.title(filename, pad=40)
    
    plt.pie(data,
            labels=['']*len(labels),
            autopct = lambda x: f'{x:.2f}%\n({(x/100)*sum(data):.2f} kWh)',
            pctdistance = 1.2)
    
    plt.legend(labels=labels,
            loc='lower right',
               bbox_to_anchor=(1, 0),
               title='Variables')
    
    plt.axis('equal')
    plt.subplots_adjust(top=1, right=0.8)  # increase margins to create more space for title and legend
    plt.tight_layout()  # automatically adjust the layout to fit the content
    
    # save the pie chart as image
    plt.savefig(OUTPUT_ANALYSIS_IMG_PATH + filename, bbox_inches='tight')

# check if csv files exists
pc_data = get_pc_data()
if pc_data is not None:
    days_in_month = get_days_in_month()
    light_mean_dict, water_mean = get_mean_watt_measured(pc_data)
    
    print("Estimated Power Consumption for 1 Container in July")
    water_power = get_water_power_consumption(water_mean, days_in_month)
    
    # store estimdated power consumption in dictionary
    estimated_power_dict = {}
    estimated_power_dict['Water'] = get_water_power_consumption(water_mean, days_in_month)
    purple_led_on_power, purple_led_off_power, white_led_on_power, white_led_off_power = get_racklight_power_consumption(1, light_mean_dict, days_in_month)
    
    estimated_power_dict['Purple LED On'] = purple_led_on_power
    estimated_power_dict['Purple LED Off'] = purple_led_off_power
    estimated_power_dict['White LED On'] = white_led_on_power
    estimated_power_dict['White LED Off'] = white_led_off_power
    
    estimated_power_dict['Aircon'] = get_aircon_power_consumption(days_in_month)
    
    # generate charts 
    generate_pie_chart(estimated_power_dict, 'Variables that Affect Monthly Power Consumption')

else:
    print("File does not exist.")
