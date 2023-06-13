import time 
import sys 
from influxdb_client import InfluxDBClient, QueryApi, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException

INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"
URL = "http://35.198.233.52:8086" 

class InfluxDBWriter:
    """Manages writing sensor data (Point) to InfluxDB Server"""
    def __init__(self, bucket_name, url=URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG):
        # Instantiates InfluxDB client, uses the Sensor Bucket by default
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket_name = bucket_name

    def set_bucket(self, bucket_name:str):
        # Modifies the bucket where R/W operations are done
        self.bucket_name = bucket_name

    def create_bucket(self, bucket_name: str, description = ""):
        # Creates a bucket based on parameters provided. Only accepts Bucket already exists error, but exits upon other erros.
        try:
            bucket = self.client.buckets_api().create_bucket(bucket_name=bucket_name, description=description)
            self.set_bucket(bucket_name)
            print(f"Successfully created: {bucket_name}")
        except ApiException as e:
            if e.status == 422 and "bucket with name" in e.body and "already exists" in e.body:
                print(f"Bucket already exists: {bucket_name}")
                self.set_bucket(bucket_name)
            else:
                print(f"Error creating bucket: {e}")
                sys.exit(1)

    def check_bucket_exists(self):
        try:
            # Get the list of buckets
            buckets = self.client.buckets_api().find_buckets()
            
            # Iterate over the buckets and check if the desired bucket name exists
            for bucket in buckets.buckets:
                if bucket.name == self.bucket_name:
                    return True
            
            # If the loop completes without finding the bucket, it doesn't exist, create it 
            print(f"Bucket '{self.bucket_name}' does not exist, attempting to create '{self.bucket_name}'")
            self.create_bucket(self.bucket_name)

        except ApiException as e:
            print(f"Error checking bucket existence: {e}")
            sys.exit(1)

    def write_single_measurement(self, measurement:Point):
        # Writes a data point (measurement) to InfluxDB Server 
        self.check_bucket_exists()
        try: 
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            write_result = write_api.write(bucket=self.bucket_name, org=self.client.org, record = measurement)
        except ApiException as e:
            print(f"Error Writing data point: {e} - {measurement}")


