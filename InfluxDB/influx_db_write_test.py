from InfluxDBWriter import InfluxDBWriter
from Sensors import SGP30SensorData, ENVHatSensorData, AirconPowerUsageSensor, GrowLightsPowerUsageSensor
import random
import time

"""
Helper script to verify InfluxDB write functionality.
Modify, INFLUXDB_TOKEN, INFLUXDB_ORG, URL and BUCKET_NAME and BUCKET_DESCRIPTION accordingly.
After running script, visit InfluxDB UI and check that values are populated correctly.
"""

# InfluxDB write client configuration
INFLUXDB_TOKEN = "mKYgBymVSgv6nIXVwrWDV1ZO0uGH-tdRlvRZ_iljh9l_nm0P8f-B95jLJfuwWAhdEimGV-2XERd_kBcELYxenw=="
INFLUXDB_ORG = "my-org"
URL = "http://34.126.186.57:8086/"
BUCKET_NAME = "Sensors (Testing)"
BUCKET_DESCRIPTION = "Testing Environment"

# Initializing simulated sensors and InfluxDB write client
sgp30_data = SGP30SensorData()  
envhat_data = ENVHatSensorData() 
growlight_data = GrowLightsPowerUsageSensor()  
aircon_data = AirconPowerUsageSensor() 

client = InfluxDBWriter(bucket_name = BUCKET_NAME, url = URL, token = INFLUXDB_TOKEN, org = INFLUXDB_ORG)  # Instantiate InfluxDB client
client.create_bucket(bucket_name = BUCKET_NAME , description = BUCKET_DESCRIPTION)
print("Sending simulated data")

# Simulating expected data from sensors, these data points will be written to influx db
sgp30_data.tvoc = 100
sgp30_data.co2 = 400
envhat_data.temperature = 17
envhat_data.humidity = 50
growlight_data.wattage = 300
aircon_data.wattage = 1000

# Popualte fileds based on simulated data above
sgp30_data.fields = sgp30_data.set_fields()
envhat_data.fields = envhat_data.set_fields()
growlight_data.fields = growlight_data.set_fields()
aircon_data.fields = aircon_data.set_fields()

# Writing data points every 10s
while True:
    # Write the sensor data to the InfluxDB server
    client.write_single_measurement(measurement=sgp30_data.create_measurement())
    client.write_single_measurement(measurement=envhat_data.create_measurement())
    client.write_single_measurement(measurement=growlight_data.create_measurement())
    client.write_single_measurement(measurement=aircon_data.create_measurement())
    time.sleep(10)  # Sleep for 10 seconds before writing to influxdb again

