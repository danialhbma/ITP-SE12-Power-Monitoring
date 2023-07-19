import pandas as pd 
import asyncio 

from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
from DataGapAlert import DataGapAlert

URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

async def main():
    influx_db_reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG) # init influxdb reader client
    telegram_alert_manager = TelegramAlertManager(influx_db_reader) # init telegram alert manager

    # Creating data gap alerts for each bucket. Alert group will be the alert_id. 
    # All classes are using evaluation interval of 6 hours. i.e., Query will retrieve all data points in bucket within the last 6 hours.
    # If number of NaN / none fields is > data_gap_threshold, a data gap alert will be sent out.
    # data_gap_threshold is 0.3 by default, evaluation_interval = '6h' by default and aggregate window= "30m" by default
    power_consumption = DataGapAlert(alert_id="Tuya Power Consumption Data Gap Alerts", bucket_name ="Power Consumption", aggregate_window_interval="1h")
    water_flow = DataGapAlert(alert_id="Water Flow Data Gap Alerts", bucket_name="Water")
    temperature = DataGapAlert(alert_id="Temperature Data Gap Alert", bucket_name="Temperature")
    humidity = DataGapAlert(alert_id="Humidity Data Gap Alerts", bucket_name="Humidity")
    co2 = DataGapAlert(alert_id="CO2 Data Gap Alerts", bucket_name="CO2")
    weather_api = DataGapAlert(alert_id="WeatherAPI Data Gap Alerts", bucket_name="WeatherAPI", aggregate_window_interval="1h")
    ambient = DataGapAlert(alert_id="Ambient Light Sensor Data Gap Alerts", bucket_name="Ambient")
    light = DataGapAlert(alert_id= "Grow Light Sensor Data Gap Alerts", bucket_name="Light")    
    
    # Adding alerts to telegram alert manager
    telegram_alert_manager.add_alert(power_consumption)
    telegram_alert_manager.add_alert(water_flow)
    telegram_alert_manager.add_alert(temperature)
    telegram_alert_manager.add_alert(humidity)
    telegram_alert_manager.add_alert(co2)
    telegram_alert_manager.add_alert(weather_api)
    telegram_alert_manager.add_alert(ambient)
    telegram_alert_manager.add_alert(light)
    
    # Execute alerts
    telegram_alert_manager.execute_alerts() # execute and evaluate alert query
    telegram_alert_manager.sort_alert_by_states() # sorts alerts into alerting, error, or nodata lists
    telegram_alert_manager.group_messages(telegram_alert_manager.alerting_list) # using self.alerting_list since we are ignoring nodata and error alerts for now (WIP)
    telegram_alert_manager.print_alert_list_details()
    await telegram_alert_manager.send_message_in_groups()
    
if __name__ == "__main__":
    asyncio.run(main())
