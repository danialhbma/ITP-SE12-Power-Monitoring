import time 
import sys 
from influxdb_client import InfluxDBClient, QueryApi, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from InfluxDBWriter import InfluxDBWriter

INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"
URL = "http://35.198.233.52:8086" 

class InfluxDBPatcher:
    def __init__(self, writer):
        """
        InfluxDB Patcher is used to patch data. Exercise caution when modifying values it is recommended to prematurely terminate the loop to ensure that updates are done correctly.
        In InfluxDB You can only update field values, to do so you must write a point with the same key (measurement, tags keys and value, time), 
        once written it will override the previous data
        """
        self.writer = writer
        self.query_api = writer.client.query_api()

    def get_zero_values(self, query):
        tables = self.query_api.query(query)
        return tables

    def patch_zero_values(self, query):
        tables = self.get_zero_values(query)

        last_non_zero_value = None
        for table in tables:
            for record in table.records:
                print(record)
                if record.get_value() == 0 and last_non_zero_value is not None:
                    new_measurement = Point(record.get_measurement())

                    # Replicate the tags
                    for tag_key in record.values.keys():
                        if tag_key.startswith('_') or tag_key == 'result' or tag_key == 'table':
                            continue  # Skip system fields
                        new_measurement.tag(tag_key, record.values.get(tag_key))

                    # Set the new field value
                    new_measurement.field(record.get_field(), last_non_zero_value)

                    # Set the timestamp
                    new_measurement.time(record.get_time())
                    print(new_measurement)
                    # sys.exit(1) # Uncomment when ready to write 
                    # self.writer.write_single_measurement(new_measurement)
                    # sys.exit(1) # Uncomment when ready to write to all  
                else:
                    last_non_zero_value = record.get_value()


# Query used to patch rack 3 grow light power consumption

query = f'''from(bucket: "Power Consumption")
  |> range(start: 2023-07-26T23:00:00Z, stop: 2023-07-27T11:00:00Z)
  |> filter(fn: (r) => r["_measurement"] == "Rack_3_Light")
  |> filter(fn: (r) => r["_field"] == "value")
'''

# Query used to patch rack 3 water pump power consumption
"""
query = f'''from(bucket: "Power Consumption")
  |> range(start: 2023-07-26T17:35:00Z, stop: 2023-07-27T16:00:00Z)
  |> filter(fn: (r) => r["_measurement"] == "Rack_3_Water")
  |> filter(fn: (r) => r["_field"] == "value")
'''
"""
writer = InfluxDBWriter("Power Consumption", URL, INFLUXDB_TOKEN, INFLUXDB_ORG)
patcher = InfluxDBPatcher(writer)
patcher.patch_zero_values(query)