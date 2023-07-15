import requests.exceptions
from influxdb_client import InfluxDBClient, QueryApi
from datetime import datetime, timedelta, timezone
import pandas as pd 
import sys
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
from DateRangeManager import DateRangeManager
from influxdb_client.rest import ApiException


"""
# TEST-SERVER
URL = "http://34.126.186.57:8086/"
INFLUXDB_TOKEN = "mKYgBymVSgv6nIXVwrWDV1ZO0uGH-tdRlvRZ_iljh9l_nm0P8f-B95jLJfuwWAhdEimGV-2XERd_kBcELYxenw=="
INFLUXDB_ORG = "my-org"
""" 

# LIVE SERVER
URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

class InfluxDBReader:
    """Serves as a Read Gateway to InfluxDB buckets"""
    def __init__(self, url=URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.query_api = QueryApi(self.client)
        self.date_range_manager = DateRangeManager()

    def _validate_query(self, start, end, aggregate_window_interval):
        try:
            self.date_range_manager.validate_date_range(start, end)
            self.date_range_manager.validate_aggregate_window(aggregate_window_interval)
        except ValueError as e:
            raise ValueError(f"Invalid query parameters: {str(e)}")
            return None

    def _create_generic_read_query(self, bucket_name:str, start:datetime, end:datetime, aggregate_window_interval) -> str:
        """Creates a flux read query to retrieve all measurements from a bucket"""
        query = f'''
        from(bucket: "{bucket_name}")
        |> range(start: {start}, stop: {end})
        |> filter(fn: (r) => r["_measurement"] != "" and r["_field"] != "weather_main") 
        |> aggregateWindow(every: {aggregate_window_interval}, fn: mean, createEmpty: false)
        '''
        # r["r_field"] != "weather_main" is a lazy fix, this is the only point in influxdb that is a string-literal
        # aggregate windows do not work on string literal types
        return query 

    def execute_query(self, query: str):
        # Executes a Flux query to retrieve data from InfluxDB
        if query is None:
            print("Empty query detected")
            return []
        try:
            tables = self.query_api.query(query)
            return tables
        except ApiException as e:
            if e.status == 404:
                print(f"Bucket not found: {e.message}")
                return []
            elif e.status == 401:
                print(f"Unauthorized access: Please verify credentials used.\nTOKEN: {INFLUXDB_TOKEN}\nORG: {INFLUXDB_ORG}\nURL:{URL}\n")
            else:
                print(e)
        except Exception as e:
            print(f"Unknown error: {e}")
            print("Flux Query Used:")
            print(query)
            return []

    def read_from_bucket(self, bucket_name, time_window, aggregate_window_interval="30m"):
        """
        Retrieves all measurements from a bucket within the specified time window.
        Args:
            bucket_name (str): The name of the bucket to read data from.
            time_window (str): The time window for querying the data. Example: "30d", "1h", "7d". e.g., 30d will retrieve all measurements from the past 30 days.
            aggregate_window_interval (str, optional): The interval for aggregating the data. Default is "30m".
        Returns:
            List: A list of tables containing the queried data.
        """
        start, end = self.date_range_manager.get_time_range(time_window)
        try:
            self._validate_query(start, end, aggregate_window_interval)
        except ValueError as e:
            print(f"Invalid query parameters provided: {start} {end} {aggregate_window_interval}\n{e}")
            return None
        
        query = self._create_generic_read_query(bucket_name, start, end, aggregate_window_interval)
        return self.execute_query(query)
        
    def query_result_to_dataframe(self, query_result) -> pd.DataFrame:
        """Converts Flux query results into a dataframe for easier manipulation"""
        df_handler = InfluxDBDataFrameHandler()
        df = df_handler.format_as_dataframe(query_result)
        if not df.empty:
            return df 
        else:
            return None

    def dataframe_to_csv(self, dataframe, output_path):
        """Exports dataframe to csv file"""
        df_handler = InfluxDBDataFrameHandler()
        try: 
             df = df_handler.export_as_csv(dataframe, output_path)
        except ValueError as e:
            print(f"Dataframe is empty: {e}")

def main():
    # Example usage 
    # (1) Initialize reader, (2) invoke read_from_bucket(bucket_name, time_window, aggregation_window) 
    # Time window must be in the format of {lenght}{unit}. e.g., "1s", "30d", "24h", "7w", "30d"
    reader = InfluxDBReader()
    co2_bucket = reader.read_from_bucket("CO2", "30d", "30m")
    print(reader.query_result_to_dataframe(co2_bucket))
    humidity_bucket = reader.read_from_bucket("Humidity", "30d", "30m")
    print(reader.query_result_to_dataframe(humidity_bucket))
    light_bucket =  reader.read_from_bucket("Light", "30d", "30m")
    print(reader.query_result_to_dataframe(light_bucket))
    power_consumption_bucket = reader.read_from_bucket("Power Consumption", "30d", "1h")
    print(reader.query_result_to_dataframe(power_consumption_bucket))
    temperature_bucket = reader.read_from_bucket("Temperature", "30d", "30m")
    print(reader.query_result_to_dataframe(temperature_bucket))
if __name__ == "__main__":
    main()
