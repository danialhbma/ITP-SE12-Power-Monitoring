from m5stack import *
from m5ui import *
from uiflow import *
from sensorinterface import SensorInterface

class WaterFlow(SensorInterface):
    def __init__(self):
        self.__adc_pin = machine.ADC(machine.Pin(36))

    def read_and_publish_data(self, publisher, rack):
        # M5TextBox(0, 16, rack, lcd.FONT_Default, 0xFFFFFF, rotate = 0)
        # M5TextBox(0, 80, "Flow: " + str(self.__adc_pin.read()), lcd.FONT_Default, 0xFFFFFF, rotate = 0)

        # publish MQTT messages
        publisher.publish_mqtt(topic = rack + "/water", data = self.__adc_pin.read())
