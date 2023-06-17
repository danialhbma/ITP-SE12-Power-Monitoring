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

    # function to reconnect to router
    def reconnect_wifi(self):
        wifiCfg.reconnect()
    
    # check if device is connected to router
    def is_connected_wifi(self):
        return wifiCfg.wlan_sta.isconnected()
    
    # function to disconnect from router
    def disconnect_wifi(self):
        wifiCfg.wlan_sta.disconnect()