# import standard
from m5stack import lcd, btnA, btnB
from m5ui import *
from uiflow import *
import machine

# import classes
from publisher import Publisher
from wifi import Wifi
from waterflow import WaterFlow
from tvoctemp import TvocTemp
from light import Light
    
# menu options
sensorOptions = ["temp/tvoc", "light", "water"]
rackOptions = ["rack1", "rack2", "rack3", "rack4"]
selectedSensor = 0
selectedRack = 0

# function to turn off all components and go into deep sleep
def deep_sleep(duration):
    # disconnect wifi
    wifi.disconnect_wifi()
    
    # disconnect from mqtt
    m5mqtt.disconnect_mqtt()
    
    # turn off lcd screen backlight
    lcd.clear()
    axp.setLcdBrightness(0)
    
    machine.deepsleep(duration)

# function to display menu options
# current option is indicated in yellow
def display_menu(menu):
    lcd.clear()
    if menu == "sensor":
        options = sensorOptions
        selected = selectedSensor
    elif menu == "rack":
        options = rackOptions
        selected = selectedRack

    M5TextBox(0, 0, "Select a " + menu + ":", lcd.FONT_Default, 0xFFFFFF, rotate = 0)
    for i, option in enumerate(options):
            color = 0xFFD700 if i == selected else 0xFFFFFF
            M5TextBox(0, (i * 20) + 50, option, lcd.FONT_Default, color, rotate = 0)

# initialise RTC to survive deepsleep
# check if user has made any selections prior to deepsleep
rtc = machine.RTC()
current = bytes(rtc.memory()).decode()

# display menu and wait for user input if user did not make any selection prior to deepsleep
# right button -> navigate to next option
# middle button -> select current option
if len(current) == 0:
    display_menu("sensor")
    while True:
        # sensor menu options
        if btnA.wasPressed() and len(current) == 0:
            current = sensorOptions[selectedSensor]
            display_menu("rack")
        elif btnB.wasPressed() and len(current) == 0:
            selectedSensor = (selectedSensor + 1) % len(sensorOptions)
            display_menu("sensor")
        # rack menu options
        elif btnA.wasPressed() and current in sensorOptions:
            current = rackOptions[selectedRack] + "/" + current
            rtc.memory(current.encode()) # store in RTC memory
            break
        elif btnB.wasPressed() and current in sensorOptions:
            selectedRack = (selectedRack + 1) % len(rackOptions)
            display_menu("rack")

lcd.clear()

# initialise Wi-Fi and publisher
wifi = Wifi()
m5mqtt = Publisher(current)
success = False

# connect to Wi-Fi and mqtt publisher if both objects exist
if wifi is not None and m5mqtt is not None:
    is_connected_wifi = wifi.connect_wifi()
    m5mqtt.connect_mqtt()
    wait(3)

    # initialise sensor if Wi-Fi is connected
    if is_connected_wifi:
        if current[-5:] == "water":
            sensor = WaterFlow()
        elif current[-5:] == "/tvoc":
            sensor = TvocTemp()
        elif current[-5:] == "light":
            sensor = Light()

        # publish data if sensor object exists
        if sensor is not None:
            sensor.read_and_publish_data(m5mqtt, current[0:5])
            success = True
            wait(2)
        
# wait for next cycle in 30 mins if all operations success, else reattempt in 5 mins
if success:
    deep_sleep(1800 * 1000)
else:
    deep_sleep(300 * 1000)
