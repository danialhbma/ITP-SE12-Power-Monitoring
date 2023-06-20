from m5stack import *
import wifiCfg
from uiflow import *

class Wifi:
    # constructor when object is initialised
    def __init__(self):
        self.__ssid = "FuzziNet"
        self.__pwd = "fauziiscute"
        
    # function to connect to router
    def connect_wifi(self):
        wifiCfg.doConnect(self.__ssid, self.__pwd)
        return self.__is_connected_wifi()
    
    # check if device is connected to router
    def __is_connected_wifi(self):
        return wifiCfg.wlan_sta.isconnected()
    
    # function to disconnect from router
    def disconnect_wifi(self):
        wifiCfg.wlan_sta.disconnect()
