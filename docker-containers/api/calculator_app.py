from flask import Flask, request, jsonify
from calculate_power_consumption import * 

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    pc_path = "Power Consumption.csv"

    # get user inputs
    num_of_purple_led_racks = int(request.json["num_of_purple_led_racks"])
    num_of_white_led_racks = int(request.json["num_of_white_led_racks"])
    aircon_cooling_capacity = request.json["aircon_cooling_capacity"]
    aircon_number_of_hours_ran = request.json["aircon_usage_per_day"]
    
    pc_data_dict, number_of_days_observed = get_pc_data(pc_path)
    if pc_data_dict is not None:
        # get estimated power consumption based on user inputs
        water_power_consumption = get_water_power_consumption(pc_data_dict,
                                                            num_of_purple_led_racks + num_of_white_led_racks)
        purple_led_power_consumption, white_led_power_consumption = get_racklight_power_consumption(pc_data_dict,
                                                                                                    num_of_purple_led_racks,
                                                                                                    num_of_white_led_racks)
        if aircon_cooling_capacity == 'Average':
            aircon_power_consumption = get_avg_aircon_power(number_of_days_observed, aircon_number_of_hours_ran)
        else:
            aircon_power_consumption = get_max_aircon_power(number_of_days_observed, aircon_number_of_hours_ran)
        
        result = water_power_consumption + purple_led_power_consumption + white_led_power_consumption + aircon_power_consumption
        
        # get current power consumption based on default values
        current_purple_racklight_power, current_white_racklight_power = get_racklight_power_consumption(pc_data_dict)
        current_power_consumption = get_water_power_consumption(pc_data_dict) + current_purple_racklight_power + current_white_racklight_power + aircon_power_consumption
        
        # get difference in power consumption
        difference = round(result - current_power_consumption, 2)
        
    else:
        result = None
        difference = None
        
    # Return result to client
    return jsonify({
        "result": result,
        "diff": difference})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) # enable on port 8080 for all available ip addresses
