import pandas as pd 
import asyncio 

from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
from DeadSensorAlert import DeadSensorAlert

URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

async def main():
    influx_db_reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG) # init influxdb reader client
    telegram_alert_manager = TelegramAlertManager(influx_db_reader) # init telegram alert manager
    
    co2 = DeadSensorAlert(alert_id="CO2 Sensor (SGP30) - Dead Sensor Alert", bucket_name="CO2")
    water_flow = DeadSensorAlert(alert_id="Water Flow Sensor (SEN0217) - Dead Sensor Alert", bucket_name="Water")
    temperature = DeadSensorAlert(alert_id = "Temperature Sensor (Env Hat) - Dead Sensor Alert", bucket_name="Temperature")
    humidity = DeadSensorAlert(alert_id="Humidity Sensor (Env Hat) - Dead Sensor Alert", bucket_name="Humidity")
    ambient = DeadSensorAlert(alert_id="Ambient Light Sensor (SEN0390) - Dead Sensor Alert", bucket_name="Ambient")
    light = DeadSensorAlert(alert_id= "M5 Light Unit - Dead Sensor Alert", bucket_name="Light")    

    # Adding alerts to telegram alert manager
    telegram_alert_manager.add_alert(co2)
    telegram_alert_manager.add_alert(water_flow)
    telegram_alert_manager.add_alert(temperature)
    telegram_alert_manager.add_alert(humidity)
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
