from m5stack import *
import wifiCfg

class Wifi:
    # constructor when object is initialised
    def __init__(self):
        # private attributes
        self.__ssid = 'FuzziNet'
        self.__pwd = 'fauziiscute'
        
    # public getters for private attributes
    def get_ssid(self):
        return self.__ssid

    def get_pwd(self):
        return self.__pwd
        
    # function to connect to router
    def connect_wifi(self):
        wifiCfg.doConnect(self.get_ssid(), self.get_pwd())

    # function to reconnect to router
    def reconnect_wifi(self):
        wifiCfg.reconnect()
    
    # check if device is connected to router
    def is_connected_wifi(self):
        return wifiCfg.wlan_sta.isconnected()
    