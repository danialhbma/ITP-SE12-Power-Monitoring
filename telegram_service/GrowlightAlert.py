from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
from InfluxDBReader import InfluxDBReader
import pandas as pd 

URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

class GrowlightOnAlert(Alert):
    def __init__(self, alert_id, threshold:int, measurement_name):
        # Alert used to determine time when growlight was switched o
        super().__init__(alert_id=alert_id, evaluation_interval="1h", alert_group="Grow Light On Alert")
        self.threshold = threshold 
        self.measurement_name = measurement_name
        self.growlight_switched_on_query()
    
    def evaluate_alert(self, wattage:float) -> None:
        # Sets the alert state based on wattage received 
        if (wattage is None):
            self.alert_state = AlertState.NODATA
            return 
        if (wattage >= threshold):
            self.alert_state = AlertState.ALERTING
        elif (wattage < threshold):
            self.alert_state = AlertState.OK
        else:
            self.alert_state = AlertState.ERROR

    def create_alert_message(self, alert_state: AlertState):
        pass
    
    def process_query_results(self, query_result):
        pass 
    
    def growlight_switched_on_query(self):
        """ Retrieves the difference in wattage between the last two data points """
        date_range_manager = DateRangeManager()
        start, end = date_range_manager.get_time_range("2h")
        query = f'''from(bucket: "Power Consumption")
            |> range(start: {start}, stop:{end})
            |> filter(fn: (r) => r["_measurement"] == "{self.measurement_name}")
            |> difference(columns: ["_value"], keepFirst: true)
            |> last()
            '''
        self.set_alert_query(query)

class GrowlightOnAlertMessage(AlertMessage):
    def __init__(self, alert_id, location):
        super().__init__(message_id=f"M-{alert_id}")
        self.location = location
        
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