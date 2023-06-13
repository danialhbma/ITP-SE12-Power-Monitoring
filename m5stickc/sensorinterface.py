from m5stack import *
from m5ui import *
from uiflow import *

class SensorInterface:
    def __init__(self):
        raise NotImplementedError
    
    def read_and_publish_data(self, publisher, rack):
        raise NotImplementedError
