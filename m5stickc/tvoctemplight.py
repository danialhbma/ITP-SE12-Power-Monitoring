from m5stack import *
from m5ui import *
from uiflow import *
from sensorinterface import SensorInterface
import hat
import unit

class TvocTempLight(SensorInterface):
    def __init__(self):
        # declare sensors -> since tvoc and light sensors are both on Port A, only 1 of them can be used at any given time on 1 m5stick
        self.__hat_env_0 = hat.get(hat.ENV)
        self.__tvoc_0 = unit.get(unit.TVOC, unit.PORTA)
        self.__light_0 = unit.get(unit.LIGHT, unit.PORTA)

    def read_and_publish_data(self, publisher, rack):
        # FOR DEBUGGING: print status on LCD
        M5TextBox(0, 16, "MQTT connected", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
        M5TextBox(0, 80, rack, lcd.FONT_Default, 0xFFFFFF, rotate = 0)

        # publish MQTT messages
        publisher.publish_mqtt(topic = rack + "/temperature", data = self.__hat_env_0.temperature)
        publisher.publish_mqtt(topic = rack + "/humidity", data = self.__hat_env_0.humidity)
        publisher.publish_mqtt(topic = rack + "/c02", data = self.__tvoc_0.eCO2)
        publisher.publish_mqtt(topic = rack + "/light", data = self.__light_0.analogValue)
        wait(1)
    