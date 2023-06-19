from m5stack import *
from m5ui import *
from uiflow import *
from sensorinterface import SensorInterface
import hat
import unit

class TvocTemp(SensorInterface):
    def __init__(self):
        # declare sensors
        self.__hat_env = hat.get(hat.ENV)
        self.__tvoc = unit.get(unit.TVOC, unit.PORTA)

    def read_and_publish_data(self, publisher, rack):
        # M5TextBox(0, 16, "MQTT connected", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
        # M5TextBox(0, 80, rack, lcd.FONT_Default, 0xFFFFFF, rotate = 0)
        
        # publish MQTT messages
        publisher.publish_mqtt(topic = rack + "/temperature", data = self.__hat_env.temperature)
        publisher.publish_mqtt(topic = rack + "/humidity", data = self.__hat_env.humidity)
        publisher.publish_mqtt(topic = rack + "/co2", data = self.__tvoc.eCO2)
        wait(2)
    