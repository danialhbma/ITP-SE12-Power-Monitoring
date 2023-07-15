from m5stack import *
from m5ui import *
from uiflow import *
from dfrobot_b_lux_v30b import DFRobot_B_LUX_V30B
from sensorinterface import SensorInterface

class Ambient(SensorInterface):
    def __init__(self):
        self.__sda = 32
        self.__scl = 33
        self.__en = 0
        self.__myLux = DFRobot_B_LUX_V30B(self.__en, self.__scl, self.__sda)
        self.__myLux.begin()

    def read_and_publish_data(self, publisher, rack):
        self.__data = self.__myLux.lightStrengthLux()

        # DEBUG
        # M5TextBox(0, 16, str(self.__data), lcd.FONT_DEFAULT, 0xFFFFFF, rotate=0)

        # publish MQTT messages
        publisher.publish_mqtt(topic = rack + "/ambient", data = self.__data)
