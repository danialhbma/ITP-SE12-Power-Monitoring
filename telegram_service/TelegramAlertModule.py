import sys
import os
from enum import Enum
from abc import ABC, abstractmethod

# Add the parent directory of InfluxDB to the system path
influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
print(influxdb_path)
sys.path.append(influxdb_path)
from InfluxDBReader import InfluxDBReader
from TelegramService import TelegramService

class AlertState(Enum):
    """ Alerts may exists in one of the following states 
    OK (no action needed), ALERTING (send telegram alert) and NODATA (no data received)"""
    OK = "OK"
    ALERTING = "ALERTING"
    NODATA = "NODATA"
    ERROR = "ERROR"

class AlertMessage(ABC):
    def __init__(self, message_id):
        """Repreesentation of the alert message that will be sent via Telegram"""
        self.message_id = message_id
        self.summary = "Alert Summary: \n"
        self.description = "Description: \n"
  
    @abstractmethod
    def format_message(self) -> str:
         raise NotImplementedError(" Subclasses must override the 'format_message' method.")
         
class Alert(ABC):
    def __init__(self, alert_id, evaluation_interval, alert_group):
        """
        alert_id: should be assigned on creation
        evaluation_interval: at which minute / hour should this alert be triggered
        alert_state: see AlertState(Enum) class
        alert_group: means to group alerts, all alert messages will be grouped by alert group
        """
        self.alert_id = alert_id
        self.evaluation_interval = evaluation_interval 
        self.alert_group = alert_group 
        self.alert_state = AlertState.OK
        self.alert_query = ""
        self.alert_message = ""
       
    def set_alert_query(self, query:str):
        """This will be query used to query data source to retrieve values for evaluation"""
        self.alert_query = query
    
    def set_alert_message(self, alert_message: AlertMessage):
        self.alert_message = AlertMessage 

    def update_alert_state(self, state:str):
        """Updates the alert state"""
        try:
            self.alert_state = AlertState(state)
        except ValueError:
            self.alert_state = AlertState("ERROR")
            print(f"Invalid alert state provided: [{state}].")

    @abstractmethod 
    def process_query_results(self, query_result): 
        """
        Accepts database query results and processes them for the subclasses to perform alert evaluation.
        """
        pass

    @abstractmethod
    def evaluate_alert(self, query_result) -> AlertState:
        """
        Accepts database parsed results and performs evaluation (threshold analysis etc.) on the results. It should return an AlertState.
        """
        raise NotImplementedError("Subclasses must override the 'evaluate_alert' method to perform alert evaluation and return an AlertState.")
    
    @abstractmethod
    def create_alert_message(self) -> AlertMessage:
        raise NotImplementedError(" Subclasses must override the 'create_alert_message' method to create and return an AlertMessage.")
    
  

    def print_alert_details(self):
        """Logging function to print Alert Object information"""
        alert_details = f"Alert ID: {self.alert_id}\n" \
                        f"Evaluation Interval: {self.evaluation_interval}\n" \
                        f"Alert Group: {self.alert_group}\n" \
                        f"Alert State: {self.alert_state}\n" \
                        f"Alert Query: {self.alert_query}\n"\
                        f"Alert Message: {self.alert_message}\n"
        print(alert_details)

class TelegramAlertManager:
    def __init__(self, db_read_client):
        """Responsible for managing a list of alerts."""
        self.alert_list = [] # contains a list of alerts to be evaluated
        self.message_list = [] # contains a list of messages that need to be sent out
        self.db_read_client = db_read_client

    def execute_alert(self, alert_query):
        pass 
    
    def populate_message_list(self):
        # TODO: From alert_list, extract all messages, group them by alert group before sending messages 
        pass

    def send_alert_message(self):
        if len(self.message_list) == 0:
            print("Message list empty")
            return 
        # TODO: Instantiate tele_client and send messages
        pass 

