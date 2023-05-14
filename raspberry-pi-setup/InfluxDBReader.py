import time 
import sys 
from influxdb_client import InfluxDBClient, QueryApi, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_TOKEN = "bkPxTXKY6zdXGWBnC8qi_-M59dCNjWQPGWGGutWhZQMC8UJ8RFfV__EqoPzehDdrDGZg68OuZJs-Wpyc15LaCA=="
INFLUXDB_ORG = "my-org"
URL = "http://172.18.0.2:8086" 

class InfluxDBReader:
    def __init__(self):
        # Instantiates InfluxDB client, uses the Sensor (Testing) Bucket by default
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.bucket_name = "Sensors (Testing)"
    
    