from m5stack import *
from m5ui import *
from uiflow import *
from m5mqtt import M5mqtt
import hat
import unit

# clear screen
setScreenColor(0x111111)

# mqtt broker details
CLIENT_ID = '11587111' # client ID must be unique for each m5stick
HOST = '326f11a4612b4a139b28c54b0c87c147.s2.eu.hivemq.cloud'
USERNAME = 'team12'
PWD = 'GiveUsAPlease12345;'

# declare sensors -> since tvoc and light sensors are both on Port A, only 1 of them can be used at any given time on 1 m5stick
hat_env_0 = hat.get(hat.ENV)
tvoc_0 = unit.get(unit.TVOC, unit.PORTA)
light_0 = unit.get(unit.LIGHT, unit.PORTA)

# labels for printing text on m5stick
label0 = M5TextBox(7, 16, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=0)

# FOR DEBUGGING: additional labels are used to display sensor data
# label1 = M5TextBox(7, 80, "label1", lcd.FONT_Default, 0xFFFFFF, rotate=0)
# label2 = M5TextBox(7, 112, "label2", lcd.FONT_Default, 0xFFFFFF, rotate=0)
# label3 = M5TextBox(7, 130, "label3", lcd.FONT_Default, 0xFFFFFF, rotate=0)
# label4 = M5TextBox(7, 150, "label4", lcd.FONT_Default, 0xFFFFFF, rotate=0)

# connect to broker and start mqtt service
# note: client ID (1st param in M5mqtt()) must be unique
m5mqtt = M5mqtt(CLIENT_ID, HOST, 8883, USERNAME, PWD, 300, ssl = True, ssl_params={'server_hostname':HOST})
m5mqtt.start()
label0.setText('publisher connected to broker')

# continually publish temperature data every second
while True:
    m5mqtt.publish(str('temperature'), str((hat_env_0.temperature)), 0)
    m5mqtt.publish(str('humidity'), str((hat_env_0.humidity)), 0)
    m5mqtt.publish(str('c02'), str((tvoc_0.eCO2)), 0)
    m5mqtt.publish(str('light'), str(light_0.digitalValue))
    
    # FOR DEBUGGING: print text on labels
    # label1.setText(str((str('temperature: ') + str((hat_env_0.temperature)))))
    # label2.setText(str((str('humidity: ') + str((hat_env_0.humidity)))))
    # label3.setText(str((str('c02: ') + str((tvoc_0.eCO2)))))
    # label4.setText(str((str('light: ') + str((light_0.digitalValue)))))
    
    wait(1)
