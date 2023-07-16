from InfluxDBReader import InfluxDBReader
from datetime import datetime
import os
import sys


INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"
URL = "http://35.198.233.52:8086" 

DATA_DIRECTORY = "data"
buckets_with_30m_intervals = ["WeatherAPI","CO2", "Humidity", "Light", "Temperature", "Water"]
buckets_with_1h_intervals = ["Power Consumption"]
"""
Helper script to retrieve bucket data as csv.
"""
if not os.path.exists(DATA_DIRECTORY):
    os.mkdir(DATA_DIRECTORY)

reader = InfluxDBReader(url = URL, token = INFLUXDB_TOKEN, org = INFLUXDB_ORG)

for bucket in buckets_with_30m_intervals:
    print(f"Retrieving data for {bucket}")
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(DATA_DIRECTORY, f"{bucket}_{current_time}.csv") 
    bucket_data = reader.read_from_bucket(bucket, "30d", "30m")
    bucket_df = reader.query_result_to_dataframe(bucket_data)
    reader.dataframe_to_csv(bucket_df, file_path)

for bucket in buckets_with_1h_intervals:
    print(f"Retrieving data for {bucket}")
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(DATA_DIRECTORY, f"{bucket}_{current_time}.csv")
    bucket_data = reader.read_from_bucket(bucket, "30d", "1h")
    bucket_df = reader.query_result_to_dataframe(bucket_data)
    reader.dataframe_to_csv(bucket_df, file_path)
