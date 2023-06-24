from m5stack import *
from m5ui import *
from uiflow import *
from sensorinterface import SensorInterface
import unit

class Light(SensorInterface):
    def __init__(self):
        # declare sensors
        self.__light = unit.get(unit.LIGHT, unit.PORTA)

    def read_and_publish_data(self, publisher, rack):
        # M5TextBox(0, 16, "MQTT connected", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
        # M5TextBox(0, 80, rack, lcd.FONT_Default, 0xFFFFFF, rotate = 0)

        # publish MQTT messages
        publisher.publish_mqtt(topic = rack + "/light", data = self.__light.analogValue)
    