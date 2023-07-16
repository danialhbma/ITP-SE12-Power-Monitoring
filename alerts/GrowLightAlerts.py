import pandas as pd 
import asyncio 

from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
from GrowlightOnAlert import GrowlightOnAlert
from GrowlightOffAlert import GrowlightOffAlert

URL = "http://35.198.233.52:8086" 
INFLUXDB_TOKEN= "n4fnErcu2V0FlN_SX6JV99UhxtsjSTV_CKA--mtv3AsVMlxG0rRx_lYyLZS03Iuc7SlmfG-kpLX9CHvwgTQBYw==" 
INFLUXDB_ORG = "my-org"

async def main():
    # Create alert rules, the threshold values were dervied from actual sensor data
    rack_1_on_alert = GrowlightOnAlert("Rack 1 Grow light On Alert", 390, "Rack_1_Light")  #
    rack_2_on_alert = GrowlightOnAlert("Rack 2 Grow light On Alert", 360, "Rack_2_Light")  #
    rack_3_on_alert = GrowlightOnAlert("Rack 3 Grow light On Alert", 270, "Rack_3_Light")  # 
    rack_1_off_alert = GrowlightOffAlert("Rack 1 Grow light Off Alert", -390, "Rack_1_Light")  #
    rack_2_off_alert = GrowlightOffAlert("Rack 2 Grow light Off Alert", -360, "Rack_2_Light")  #
    rack_3_off_alert = GrowlightOffAlert("Rack 3 Grow light Off Alert", -270, "Rack_3_Light") #

    influx_db_reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG) # init influxdb reader client
    telegram_alert_manager = TelegramAlertManager(influx_db_reader) # init telegram alert manager

    telegram_alert_manager.add_alert(rack_1_on_alert)
    telegram_alert_manager.add_alert(rack_2_on_alert)
    telegram_alert_manager.add_alert(rack_3_on_alert)
    telegram_alert_manager.add_alert(rack_1_off_alert)
    telegram_alert_manager.add_alert(rack_2_off_alert)
    telegram_alert_manager.add_alert(rack_3_off_alert)
    telegram_alert_manager.execute_alerts()
    telegram_alert_manager.sort_alert_by_states()
    telegram_alert_manager.group_messages(telegram_alert_manager.alerting_list) # using self.alerting_list since we do not want to send out nodata alerts
    telegram_alert_manager.print_alert_list_details()
    await telegram_alert_manager.send_message_in_groups()
    
if __name__ == "__main__":
    asyncio.run(main())