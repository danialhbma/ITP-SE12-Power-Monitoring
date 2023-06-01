from m5stack import *
from m5ui import *
from uiflow import *
from m5mqtt import M5mqtt
import hat
import unit
import machine

# clear screen
setScreenColor(0x111111)

# mqtt broker details
CLIENT_ID = 'rack1_temperature&c02' # client ID must be unique for each m5stick
HOST = '34.124.179.126'
USERNAME = 'admin'
PWD = 'changemeplease'
PORT = 1883

# declare sensors -> since tvoc and light sensors are both on Port A, only 1 of them can be used at any given time on 1 m5stick
hat_env_0 = hat.get(hat.ENV)
tvoc_0 = unit.get(unit.TVOC, unit.PORTA)
light_0 = unit.get(unit.LIGHT, unit.PORTA)

# function to connect to MQTT broker and start MQTT service
def connect_mqtt():
    global m5mqtt
    m5mqtt = M5mqtt(CLIENT_ID, HOST, PORT, USERNAME, PWD, keepalive=300, ssl=False, ssl_params=None)
    m5mqtt.start()

# connect to MQTT broker and start MQTT service
connect_mqtt()

mqttConnected = True
      
# publish data every hour using qos 0
while True:
    # check if connected to MQTT broker
    if not mqttConnected:
        connect_mqtt()
        
    # publish MQTT messages
    m5mqtt.publish(str('rack1/temperature'), str(hat_env_0.temperature), qos=1)
    m5mqtt.publish(str('rack1/humidity'), str(hat_env_0.humidity), qos=1)
    m5mqtt.publish(str('rack1/c02'), str(tvoc_0.eCO2), qos=1)
    m5mqtt.publish(str('rack1/light'), str(light_0.analogValue), qos=1)
    
    wait(5)
    
    # Enter deep sleep mode for 1 hour (3600 seconds) to conserve power
    machine.deepsleep(3600 * 1000)  # Sleep for 1 hour (3600 seconds) in milliseconds
