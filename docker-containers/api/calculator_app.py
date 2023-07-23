from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    # To replace with actual input and formula
    aircon_power_consumption = request.json["aircon_input"]
    light_power_consumption = request.json["light_input"]
    water_power_consumption =  request.json["water_input"]
    result = aircon_power_consumption + light_power_consumption + water_power_consumption

    # Return result to client
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080) # enable on port 8080 for all available ip addresses
