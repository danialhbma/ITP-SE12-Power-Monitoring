from m5stack import *
from m5mqtt import M5mqtt

class Publisher:
    # constructor when object is initialised
    def __init__(self, client_id):
        # private attributes
        self.__host = '35.197.144.239'
        self.__username = 'admin'
        self.__pwd = 'changemeplease'
        self.__port = 1883

        # public attribute
        self.client = M5mqtt(client_id, 
                             self.__host, 
                             self.__port, 
                             self.__username, 
                             self.__pwd, 
                             keepalive = 300, 
                             ssl = False, 
                             ssl_params = None)

    # function to connect to MQTT broker and start MQTT service
    def connect_mqtt(self):
        self.m5_client.start()
        return True

    # function to publish data to respective topic
    def publish_mqtt(self, topic, data):
        self.m5_client.publish(str(topic), str(data), qos = 1)
