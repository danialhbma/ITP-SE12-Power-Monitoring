from m5stack import *
from m5ui import *
from uiflow import *
from publisher import Publisher
import hat
import unit
import machine

# clear screen
setScreenColor(0x111111)

# declare sensors -> since tvoc and light sensors are both on Port A, only 1 of them can be used at any given time on 1 m5stick
hat_env_0 = hat.get(hat.ENV)
tvoc_0 = unit.get(unit.TVOC, unit.PORTA)
light_0 = unit.get(unit.LIGHT, unit.PORTA)

# FOR DEBUGGING: labels for printing text on m5stick
label0 = M5TextBox(7, 16, "label0", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
label1 = M5TextBox(7, 80, "label1", lcd.FONT_Default, 0xFFFFFF, rotate = 0)

# initialise MQTT publisher object
m5mqtt = Publisher("rack1_temp_co2")
is_connected = False

# publish data every hour using qos 0
while True:
    # check if connected to MQTT broker
    if is_connected():
        # FOR DEBUGGING: print status on LCD
        label0.setText("MQTT connected")

        # publish MQTT messages
        m5mqtt.publish_mqtt(topic = "rack1/temperature", data = hat_env_0.temperature)
        m5mqtt.publish_mqtt(topic = "rack1/humidity", data = hat_env_0.humidity)
        m5mqtt.publish_mqtt(topic = "rack1/c02", data = tvoc_0.eCO2)
        m5mqtt.publish_mqtt(topic = "rack1/light", data = light_0.analogValue)
        wait(1)

    # connect to MQTT broker and start MQTT service
    else:
        label0.setText("MQTT disconnected")
        is_connected = m5mqtt.connect_mqtt()
    
    # Enter deep sleep mode for 1 hour (3600 seconds) to conserve power
    machine.deepsleep(3600 * 1000)  # 1 hour in milliseconds
