from m5stack import *
from m5mqtt import M5mqtt
from uiflow import *

class Publisher:
    # constructor when object is initialised
    def __init__(self, client_id):
        self.__client = M5mqtt(client_id,
                             "35.198.233.52", # host
                             1883, # port
                             "admin", # username
                             "changemeplease", # pwd
                             keepalive = 300,
                             ssl = False,
                             ssl_params = None)

    # function to connect to MQTT broker and start MQTT service
    def connect_mqtt(self):
        self.__client.start()

    # function to publish data to respective topic
    def publish_mqtt(self, topic, data):
        self.__client.publish(str(topic), str(data), qos = 1)
