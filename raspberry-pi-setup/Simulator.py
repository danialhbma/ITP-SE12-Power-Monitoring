from InfluxDBWriter import InfluxDBWriter
from Sensors import SGP30SensorData, ENVHatSensorData, AirconPowerUsageSensor, GrowLightsPowerUsageSensor
import random
import time

sgp30_data = SGP30SensorData(0, 0)  # Initialize with 0 values
envhat_data = ENVHatSensorData(0, 0, 0, 0)  # Initialize with 0 values
growlight_data = GrowLightsPowerUsageSensor(0)  # Initialize with 0 value
aircon_data = AirconPowerUsageSensor(0)  # Initialize with 0 value
client = InfluxDBWriter()  # Instantiate InfluxDB client
client.create_bucket(bucket_name = "Sensors (Testing)", description = "Testing Environment")

print("Sending simulated data")
counter = 0
while True:
    # Generate random values within a certain range for the sensor readings
    sgp30_data.tvoc = random.randint(0, 200)
    sgp30_data.co2 = random.randint(0, 2000)
    envhat_data.temperature = round(random.uniform(20, 30), 1)
    envhat_data.humidity = round(random.uniform(30, 60), 1)
    envhat_data.air_pressure = round(random.uniform(1000, 1100), 1)
    envhat_data.mag_field = random.randint(1000, 2000)

    # Increment the power usage sensor readings by a certain amount
    growlight_data.wattage += 1
    aircon_data.wattage += 5

    # Call set_fields() to update the values before creating sensor data
    sgp30_data.fields = sgp30_data.set_fields()
    envhat_data.fields = envhat_data.set_fields()
    growlight_data.fields = growlight_data.set_fields()
    aircon_data.fields = aircon_data.set_fields()

    # Write the sensor data to the InfluxDB server
    client.write_single_measurement(sensor_data=sgp30_data.create_sensor_data())
    client.write_single_measurement(sensor_data=envhat_data.create_sensor_data())
    client.write_single_measurement(sensor_data=growlight_data.create_sensor_data())
    client.write_single_measurement(sensor_data=aircon_data.create_sensor_data())
    time.sleep(1)  # Sleep for 1 second before looping again
    
    counter += 1
    if (counter%60 == 0):
        print(f"Time elapsed: {counter//60}")
