from m5stack import *
from m5ui import *
from uiflow import *
from publisher import Publisher
from wifi import Wifi
import hat
import unit
import machine

# clear screen
setScreenColor(0x111111)

# FOR DEBUGGING: labels for printing text on m5stick
label0 = M5TextBox(7, 16, "label0", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
label1 = M5TextBox(7, 80, "label1", lcd.FONT_Default, 0xFFFFFF, rotate = 0)

# FOR DEBUGGING: print status on LCD
label0.setText("Wifi disconnected")

# Connect to Wi-Fi
wifi = Wifi()
wifi.connect_wifi()

# if wifi is not connected, put device to sleep and try again in 5 mins
if not wifi.is_connected_wifi():
    label0.setText("Wifi disconnected")
    
    wifi.reconnect_wifi()
    
    # Enter deep sleep mode for 5 mins (300 seconds) to conserve power
    machine.deepsleep(300 * 1000)  # 5 mins in milliseconds
    
else:
    label0.setText("Wifi connected")
    
    # declare sensors -> since tvoc and light sensors are both on Port A, only 1 of them can be used at any given time on 1 m5stick
    hat_env_0 = hat.get(hat.ENV)
    tvoc_0 = unit.get(unit.TVOC, unit.PORTA)
    light_0 = unit.get(unit.LIGHT, unit.PORTA)
    
    # initialise MQTT publisher object
    m5mqtt = Publisher("rack1_temp_co2")
    is_connected = m5mqtt.connect_mqtt()
        
    # check if connected to MQTT broker
    if is_connected:
        label1.setText("MQTT connected")

        # publish MQTT messages
        m5mqtt.publish_mqtt(topic = "rack1/temperature", data = hat_env_0.temperature)
        m5mqtt.publish_mqtt(topic = "rack1/humidity", data = hat_env_0.humidity)
        m5mqtt.publish_mqtt(topic = "rack1/c02", data = tvoc_0.eCO2)
        m5mqtt.publish_mqtt(topic = "rack1/light", data = light_0.analogValue)
        wait(1)

    # connect to MQTT broker and start MQTT service
    else:
        label1.setText("MQTT disconnected")
        is_connected = m5mqtt.connect_mqtt()
    
    # Enter deep sleep mode for 1 hour (3600 seconds) to conserve power
    machine.deepsleep(3600 * 1000)  # 1 hour in milliseconds
