import os 
import sys 
import pandas as pd

influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBReader import InfluxDBReader
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler

# LIVE SERVER
URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

def main():
    reader = InfluxDBReader()
    historical_power_consumption = reader.read_from_bucket("Historical Power Consumption", "30d", "30m")
    print(reader.query_result_to_dataframe(historical_power_consumption))

if __name__ == "__main__":
    main()