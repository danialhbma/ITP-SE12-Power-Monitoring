from datetime import datetime
import os
import sys
influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
from InfluxDBReader import InfluxDBReader

INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"
URL = "http://35.198.233.52:8086" 

DATA_DIRECTORY = "data" # Folder where csvs will be extracted to
if not os.path.exists(DATA_DIRECTORY):
    os.mkdir(DATA_DIRECTORY)

"""
Helper script to retrieve bucket data as csv.
"""

def extract_raw_data(buckets:list, reader: InfluxDBReader, date_range = "45d", aggregation_window_interval = "30m"):
    """
    Helper function to retrieve and extract data from InfluxDB and store them as .csv files.

    Parameters:
        buckets (list): List of bucket names to retrieve data for.
        date_range (str, optional): Date range for the data retrieval (e.g., "45d" for 45 days). Defaults to "45d".
        aggregation_window_interval (str, optional): Aggregation window interval (e.g., "30m" for 30 minutes). Defaults to "30m".
    """
    for bucket in buckets:
        print(f"Retrieving data for {bucket}")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(DATA_DIRECTORY, f"{bucket}.csv")
        bucket_data = reader.read_from_bucket(bucket, date_range, aggregation_window_interval) # Change window accordingly, it should cover the dates of all points of interest
        bucket_df = reader.query_result_to_dataframe(bucket_data)
        reader.dataframe_to_csv(bucket_df, file_path)

# Extracting data from all our buckets in InfluxDB server
buckets_with_30m_intervals = ["WeatherAPI","CO2", "Humidity", "Light", "Temperature", "Water"]
buckets_with_1h_intervals = ["Power Consumption"]
buckets_with_1m_intervals = ["Ambient"]
historical_buckets = ["Historical Weather Data", "Historical Power Consumption"] 

reader = InfluxDBReader(url = URL, token = INFLUXDB_TOKEN, org = INFLUXDB_ORG)
extract_raw_data(buckets_with_30m_intervals, reader)
extract_raw_data(buckets_with_1h_intervals, reader, aggregation_window_interval="1h")
extract_raw_data(buckets_with_1m_intervals, reader, aggregation_window_interval="1m")
extract_raw_data(historical_buckets, reader, date_range="100d")
