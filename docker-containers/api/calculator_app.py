from flask import Flask, request, jsonify
from calculate_power_consumption import * 

app = Flask(__name__)

# calculates power consumption for 1 rack
@app.route("/rack_calculator", methods=["POST"])
def rack_calculator():
    pc_path = "Power Consumption.csv"
    pc_data = get_pc_data(pc_path)

    if pc_data is not None:  
        # get user inputs
        colour_of_led = request.json["colour_of_led"]
        led_usage_hours = request.json["led_usage_hours"]
        water_usage_hours = request.json["water_usage_hours"]
        num_of_days = request.json["num_of_days"]
        
        led_wattage = int(request.json["led_wattage"])
        water_wattage = int(request.json["water_wattage"])
        cost_per_kwh = float(request.json["cost_per_kwh"])
        
        light_mean_dict, water_mean = get_mean_watt_measured(pc_data)
        
        if water_wattage != 0:
            # calculate water power consumption based on user input values
            water_power = get_water_power_consumption(water_wattage, num_of_days, water_usage_hours, 1)
        else:
            # calculate water power consumption based on measured values
            water_power = get_water_power_consumption(water_mean, num_of_days, water_usage_hours, 1) 
        
        if led_wattage != 0:
            # calculate LED power consumption based on user input values
            led_power = calculate_power_from_watts(led_wattage, num_of_days, led_usage_hours, 1)
            result = led_power + water_power
        
        else:
            purple_led_power, white_led_power = get_racklight_power_consumption(0,
                                                                                light_mean_dict,
                                                                                num_of_days,
                                                                                led_usage_hours,
                                                                                led_usage_hours,
                                                                                1, 1)
        
            # return power consumption based on selected led colour
            if colour_of_led == "Purple":
                result = purple_led_power + water_power 
            else:
                result = white_led_power + water_power

        result = round(result, 2)
        
        # calculate cost
        if cost_per_kwh > 0:
            cost = calculate_cost(result, cost_per_kwh)
        else:
            cost = calculate_cost(result)
        
    else:
        result = "Error"
        cost = "Error"
        
    # Return result to client
    return jsonify({
        "result": result,
        "cost": cost
        })

# calculate power consumption of container for 1 month if conditions are altered
@app.route("/container_calculator", methods=["POST"])
def container_calculator():
    pc_path = "Power Consumption.csv"
    pc_data = get_pc_data(pc_path)
    
    if pc_data is not None:
        # purple led
        num_of_purple_led_racks = int(request.json["num_of_purple_led_racks"])
        purple_led_usage_hours = request.json["purple_led_usage_hours"]
        purple_led_wattage = int(request.json["purple_led_wattage"])
        
        # white led
        num_of_white_led_racks = int(request.json["num_of_white_led_racks"])
        white_led_usage_hours = request.json["white_led_usage_hours"]
        white_led_wattage = int(request.json["white_led_wattage"])
        
        # water pump
        water_usage_hours = request.json["water_usage_hours"]
        water_wattage = int(request.json["water_wattage"])
        
        # aircon
        aircon_usage = request.json["aircon_usage_hours"]
        num_aircon_units = int(request.json["num_aircon_units"])
        aircon_wattage = int(request.json["aircon_wattage"])
        
        # cost
        cost_per_kwh = float(request.json["cost_per_kwh"])
        
        # get days in current month 
        days_in_month = get_days_in_month()
        light_mean_dict, water_mean = get_mean_watt_measured(pc_data)
        
        # get water pump power consumption
        current_water_power = get_water_power_consumption(water_mean, days_in_month)
        if water_wattage != 0:
            # calculate water power consumption based on user input values
            simulated_water_power = get_water_power_consumption(water_wattage, days_in_month, water_usage_hours, 1)
        else:
            # calculate water power consumption based on measured values
            simulated_water_power = get_water_power_consumption(water_mean, days_in_month, water_usage_hours, 1) 
        
        # get rack light power consumption
        current_purple_led, current_white_led = get_racklight_power_consumption(0, light_mean_dict, days_in_month)
        current_light_power = current_purple_led + current_white_led
        if purple_led_wattage != 0:
            # use inputted wattage values to calculate LED power consumption
            simulated_purple_led_power = calculate_power_from_watts(purple_led_wattage, days_in_month, purple_led_usage_hours, num_of_purple_led_racks)
            simulated_white_led_power = calculate_power_from_watts(white_led_wattage, days_in_month, white_led_usage_hours, num_of_white_led_racks)
        else:
            # use user variables but default wattage to calculate LED power consumption
            simulated_purple_led_power, simulated_white_led_power = get_racklight_power_consumption(0,
                                                                                light_mean_dict,
                                                                                days_in_month,
                                                                                purple_led_usage_hours,
                                                                                white_led_usage_hours,
                                                                                num_of_purple_led_racks,
                                                                                num_of_white_led_racks)
        simulated_light_power = simulated_purple_led_power + simulated_white_led_power
        
        # get aircon power consumption
        if aircon_wattage != 0:
            # use inputted wattage values to calculate aircon power consumption
            simulated_aircon_power = get_aircon_power_consumption(days_in_month, aircon_usage, num_aircon_units, aircon_wattage)
        else:
            # use user variables but default wattage to calculate aircon power consumption
            simulated_aircon_power = get_aircon_power_consumption(days_in_month, aircon_usage, num_aircon_units)
            
        current_aircon_power = get_aircon_power_consumption(days_in_month)
        
        result = simulated_water_power + simulated_light_power + simulated_aircon_power
        current_power_consumption = current_water_power + current_light_power + current_aircon_power
        
        difference = result - current_power_consumption
        
        # calculate cost
        if cost_per_kwh > 0:
            cost = calculate_cost(result, cost_per_kwh)
            cost_diff = calculate_cost(difference, cost_per_kwh)
            
        else:
            cost = calculate_cost(result)
            cost_diff = calculate_cost(difference)
            
    else:
        result, difference, cost, cost_diff = "Error"
        
    # Return result to client
    return jsonify({
        "result": result,
        "diff": difference,
        "cost": cost,
        "cost_diff": cost_diff})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) # enable on port 8080 for all available ip addresses
