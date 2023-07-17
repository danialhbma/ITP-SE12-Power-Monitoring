import pandas as pd
import os 
import sys 

influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
from InfluxDBReader import InfluxDBReader

DATA_DIRECTORY = "data"


class ExternalConditionsDataFrame(InfluxDBDataFrameHandler):
    def __init__(self, csv_file):
        self.dataframe = self.load_from_csv(csv_file)
    
    def get_unique_fields(self) -> list:
        self.unique_fields = self.get_unique_values(self.dataframe, "_field")
    
def main():
    external_condition = ExternalConditionsDataFrame(source)
    external_condition.get_unique_fields()

    for field in external_condition.unique_fields:
        print(external_condition.get_slice(external_condition.dataframe, field))

if __name__ == "__main__":
        main()

