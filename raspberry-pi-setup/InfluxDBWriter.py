import time 
import sys 
from influxdb_client import InfluxDBClient, QueryApi, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


INFLUXDB_TOKEN = "bkPxTXKY6zdXGWBnC8qi_-M59dCNjWQPGWGGutWhZQMC8UJ8RFfV__EqoPzehDdrDGZg68OuZJs-Wpyc15LaCA=="
INFLUXDB_ORG = "my-org"
URL = "http://172.18.0.2:8086" 

class InfluxDBWriter:
    """Manages writing sensor data (Point) to InfluxDB Server"""
    def __init__(self, url=URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG):
        # Instantiates InfluxDB client, uses the Sensor Bucket by default
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket_name = "Sensors (Testing)"

    def set_bucket(self, bucket_name:str):
        # Modifies the bucket where R/W operations are done
        self.bucket_name = bucket_name

    def create_bucket(self, bucket_name:str, description:str):
        # Creates a new bucket, a Bucket contains one or more measurements, measurements contain one or more fields and tags
        try:
            bucket = self.client.buckets_api().create_bucket(bucket_name=bucket_name, description = description)
            self.set_bucket(bucket_name)
            print(f"Successfully created: {bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")
            sys.exit(1)

    def write_single_measurement(self, sensor_data:Point):
        # Writes a data point (measurement) to InfluxDB Cloud Server 
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self.bucket_name, org=self.client.org, record = sensor_data)

    def write_batch_measurement(self, sensor_data_list: list[Point]):
        # TODO: Create function that can perform writing in batches or in intervals. This way wont have to keep sending every X-seconds / X-minute.
        pass

    def delete_measurement(self, measurement_name):
        # TODO: Deletes data from bucket 
        pass


