import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from calculate_power_consumption import *

# constants
OUTPUT_ANALYSIS_IMG_PATH = "./results/"

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
pc_data_dict, number_of_days_observed = get_pc_data()
if pc_data_dict is not None:
    # store estimdated power consumption in dictionary
    estimated_pc_dict = {}
    purple_racklight, white_racklight = get_racklight_power_consumption(pc_data_dict,
                                                                        NUM_OF_PURPLE_LED_RACKS,
                                                                        NUM_OF_WHITE_LED_RACKS)
    estimated_pc_dict['Water'] = get_water_power_consumption(pc_data_dict,
                                                             NUM_OF_PURPLE_LED_RACKS + NUM_OF_WHITE_LED_RACKS)
    estimated_pc_dict['Purple LED Rack Lights'] = purple_racklight
    estimated_pc_dict['White LED Rack Lights'] = white_racklight
    estimated_pc_dict['Aircon (Average Capacity)'] = get_avg_aircon_power(number_of_days_observed)
    
    # generate charts for both average and max capacity
    generate_pie_chart(estimated_pc_dict, 'Variables that Affect Monthly Power Consumption - Average Capacity')
    
    estimated_pc_dict.pop("Aircon (Average Capacity)", None)
    estimated_pc_dict['Aircon (Max Capacity)'] = get_max_aircon_power(number_of_days_observed)
    generate_pie_chart(estimated_pc_dict, 'Variables that Affect Monthly Power Consumption - Max Capacity')

else:
    print("File does not exist.")
