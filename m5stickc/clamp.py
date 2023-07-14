from m5stack import *
from m5ui import *
from uiflow import *
from sensorinterface import SensorInterface
import machine

class Clamp(SensorInterface):
    def __init__(self):
        self.__adc_pin = machine.ADC(machine.Pin(36))
        self.__ac_range = 5 # SEN0287 uses AC transformer range of 5A

        # Since the analog reading is affected by the accuracy of the reference voltage.
        # For a more accurate reading, use a high-precision multimeter to measure the 
        # analog reference voltage of the controller (usually the same as the supply voltage) and 
        # modify self.__vref below to complete the calibration.
        self.__vref = 5.0 # assumption as Vout = 5V

    def read_and_publish_data(self, publisher, rack):
        # retrieve the peak voltage
        self.__peak_voltage = 0
        for _ in range(5):
            self.__peak_voltage += self.__adc_pin.read()
            wait(1)

        self.__peak_voltage /= 5

        # calculate current and power
        self.__vrms = self.__peak_voltage * 0.707
        self.__vrms = (self.__vrms / 1024 * self.__vref) / 2 # circuit is amplied by 2x, thus divide by 2
        self.__ac_current = self.__vrms * self.__ac_range
        self.__power = self.__ac_current * 240

        # DEBUG
        M5TextBox(0, 16, str(self.__power), lcd.FONT_Default, 0xFFFFFF, rotate = 0)

        # publish MQTT messages
        # publisher.publish_mqtt(topic = rack + "/clamp", data = self.__power)
