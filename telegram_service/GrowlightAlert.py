from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
from InfluxDBReader import InfluxDBReader
import pandas as pd 

URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

class GrowlightOnAlert(Alert):
    def __init__(self, alert_id, threshold:int, measurement_name):
        super().__init__(alert_id=alert_id, evaluation_interval="1h", alert_group="Grow light On Alert")
        self.threshold = threshold 
        self.measurement_name = measurement_name
        self.growlight_switched_on_query()

    def evaluate_alert(self, query_result) -> AlertState:
        pass

    def create_alert_message(self):
        pass
    
    def growlight_switched_on_query(self):
        # Obtains the difference between the 2 latest data points
        date_range_manager = DateRangeManager()
        start, end = date_range_manager.get_time_range("1d")
        query = f'''from(bucket: "Power Consumption")
            |> range(start: {start}, stop:{end})
            |> filter(fn: (r) => r["_measurement"] == "{self.measurement_name}")
            |> difference(columns: ["_value"], keepFirst: true)
            '''
        self.set_alert_query(query)

    def get_wattage_difference(self):

class GrowlightOffAlert(Alert):
    def __init__(self, threshold):
        self.threshold = threshold 
    def evaluate_alert(self, query_result) -> AlertState:
        pass 
    def create_alert_message(self) -> AlertMessage:
        pass

def main():
    rack_1_on_alert = GrowlightOnAlert(1, 360, "Rack_1_Light")
    # rack_2_on_alert = GrowlightOnAlert(2, 350, "Rack_2_Light")
    # rack_3_on_alert = GrowlightOnAlert(3, 240, "Rack_3_Light")

    influx_db_reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG)
    results = influx_db_reader.execute_query(rack_1_on_alert.alert_query)
    print(influx_db_reader.query_result_to_dataframe(results))
    rack_1_on_alert.print_alert_details()

if __name__ == "__main__":
    main()