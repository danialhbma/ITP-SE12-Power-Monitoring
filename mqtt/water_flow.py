from m5stack import *
from m5ui import *
from uiflow import *
from publisher import Publisher
import machine

# clear screen
setScreenColor(0x111111)

# declare sensors
adc_pin = machine.ADC(machine.Pin(36))

# FOR DEBUGGING: labels for printing text on m5stick
label0 = M5TextBox(7, 16, "label0", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
label1 = M5TextBox(7, 80, "label1", lcd.FONT_Default, 0xFFFFFF, rotate = 0)

# initialise mqtt publisher object
m5mqtt = Publisher("water")
is_connected = False

# main program
while True:
    # proceed if connected to MQTT broker
    if is_connected:
        data = adc_pin.read()

        # FOR DEBUGGING: print status on LCD
        label0.setText("MQTT connected")
        label1.setText("Flow: %s", str(data))

        # publish MQTT messages
        m5mqtt.publish_mqtt(topic = "water", data = data)
        wait(1)
    
    # connect to MQTT broker and start MQTT service
    else:
        label0.setText("MQTT disconnected")
        is_connected = m5mqtt.connect_mqtt()

    # Enter deep sleep mode for 30 mins (1800 seconds) to conserve power
    machine.deepsleep(1800 * 1000)  # 1/2 hour in milliseconds
