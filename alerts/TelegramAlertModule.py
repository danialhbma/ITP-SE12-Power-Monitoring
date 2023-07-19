import sys
import os
from enum import Enum
from abc import ABC, abstractmethod

# Add the parent directory of InfluxDB and TelegramService to the system path
influxdb_path = os.path.abspath(os.path.join("..", "InfluxDB"))
sys.path.append(influxdb_path)
from InfluxDBReader import InfluxDBReader
from InfluxDBDataFrameHandler import InfluxDBDataFrameHandler
telegram_service_path = os.path.abspath(os.path.join("..", "telegram_service"))
sys.path.append(telegram_service_path)
from TelegramService import TelegramService

"""
The TelegramAlertModule contains classes and functions related to managing alerts and sending alert messages via Telegram.
AlertState: Enum class representing the possible states of an alert (OK, ALERTING, NODATA, ERROR).
AlertMessage: Abstract base class representing the structure of an alert message. Subclasses must implement the format_message method.
Alert: Abstract base class representing an alert. Subclasses must implement the evaluation and _create_alert_message methods.
TelegramAlertManager: Class responsible for managing a list of alerts, executing alert evaluations, grouping messages, and sending alerts via Telegram.
"""

class AlertState(Enum):
    """ 
    Alerts may exists in one of the following states 
    OK (no action needed), ALERTING (send telegram alert) and NODATA (no data received)
    """
    OK = "OK"
    ALERTING = "ALERTING"
    NODATA = "NODATA"
    ERROR = "ERROR"

class AlertMessage():
    def __init__(self, message_id):
        """Repreesentation of the alert message that will be sent via Telegram"""
        self.message_id = message_id
        self.summary = "Alert Summary: "
        self.description = "Description: "
        self.message = ""
  
    @abstractmethod
    def format_message(self) -> str:
         raise NotImplementedError(" Subclasses must override the 'format_message' method.")
    
class Alert(ABC):
    def __init__(self, alert_id, evaluation_interval, alert_group, active_state = True):
        """
        alert_id: alert name
        evaluation_interval: at which minute / hour should this alert be triggered
        alert_state: see AlertState(Enum) class
        alert_group: means to group alerts, all alert messages will be grouped by alert group
        is_active: used to activate / inactive alerts. Only active alerts will be evaluated. Set to active by defauly
        """
        self.alert_id = alert_id # rename to alert_name
        self.evaluation_interval = evaluation_interval 
        self.alert_group = alert_group 
        self.alert_state = AlertState.OK
        self.alert_query = ""
        self.alert_message = ""

    def set_alert_query(self, query:str):
        """This will be query used to query data source to retrieve values for evaluation"""
        self.alert_query = query
    
    def set_alert_message(self, alert_message: AlertMessage):
        self.alert_message = alert_message

    def update_alert_state(self, state:str):
        """Updates the alert state"""
        try:
            self.alert_state = AlertState(state)
        except ValueError:
            self.alert_state = AlertState("ERROR")
            print(f"Invalid alert state provided: [{state}].")

    @abstractmethod
    def evaluation(self, query_result):
        """
        Should contain all alert business logic i.e., evaluating of alert and updateing of alert state
        """
        raise NotImplementedError("Subclasses must override the 'evaluation' method to perform alert evaluation and return an AlertState.")

    @abstractmethod
    def _create_alert_message(self) -> AlertMessage:
        """Creates an empty alert message"""
        raise NotImplementedError("Subclasses must override the 'evaluation' method to perform alert evaluation and return an AlertState.")
    
    def print_alert_details(self):
        """Logging function to print Alert Object information"""
        alert_details = f"Alert ID: {self.alert_id}\n" \
                        f"Evaluation Interval: {self.evaluation_interval}\n" \
                        f"Alert Group: {self.alert_group}\n" \
                        f"Alert State: {self.alert_state}\n" \
                        f"Alert Query: {self.alert_query}\n"
        try:
            alert_details += f"{self.alert_message.message}\n"
        except AttributeError as e:
            print(f"AlertMessageObject not created: {e}")

        print(alert_details)

class TelegramAlertManager:
    def __init__(self, db_read_client):
        """Responsible for managing a list of alerts."""
        self.alert_list = [] # contains all alerts to be evaluated
        self.db_read_client = db_read_client # influx db read client

        self.alerting_list = [] # alerts that require telegram notification (ALERTING state)
        self.nodata_list = [] # alerts in nodata state 
        self.error_list = [] # alerts in an error state 

        self.alert_group_messages = {} # used to group messages together, {alert_id}:{message1\n message2 \nmessage3}
    def _validate_alert(self, alert:Alert):
        """Ensures that object is an Alert subclass before appending to alert list"""
        if alert is None:
            raise ValueError("None type object")
        if not isinstance(alert, Alert):
            raise TypeError("Expected Alert or its subclass.")

    def add_alert(self, alert: Alert):
        """Adds alert to alert list"""
        try:
            self._validate_alert(alert)
            self.alert_list.append(alert)
        except ValueError as e:
            print(f"Invalid Alert type: {e}")
            return 
        except TypeError as e:
             print(f"Invalid Alert type: {e}")
             return 

    def print_alert_list_details(self):
        """Logging function to log all alert information"""
        if len(self.alert_list) == 0:
            print("No alerts found in alert list.")
            return 

        for alert in self.alert_list:
            alert.print_alert_details()

    def execute_alerts(self):
        """Executes all queries for alerts within alert list"""
        for alert in self.alert_list:
            query_result = self._execute_alert(alert.alert_query)
            alert.evaluation(query_result)

    def _execute_alert(self, alert_query):
        results = self.db_read_client.execute_query(alert_query)
        return results
        
    def group_messages(self, alert_list) -> dict:
        """ 
        Iterates through a list of list of alerts and groups alerts based on their alert_group.
        Alerts belonging to the same alert group, will be grouped into 1 telegram message.
        """
        for alert in alert_list:
            if alert.alert_state == AlertState.OK:
                # AlertState.OK indicate that no alerting is required OR alert has already been fired i.e., FIRING -> OK or NODATA -> OK
                continue 
                
            if alert.alert_group not in self.alert_group_messages.keys():
                self.alert_group_messages[alert.alert_group] = alert.alert_message.message
                self.alert_group_messages[alert.alert_group] += "\n\n"
            else: 
                self.alert_group_messages[alert.alert_group] += alert.alert_message.message
                self.alert_group_messages[alert.alert_group] += "\n\n"
    
    def sort_alert_by_states(self): 
        """ 
        Sort alerts based on their state, populates the corresponding list with the alerts
        """   
        for alert in self.alert_list:
            if alert.alert_state == AlertState.ALERTING:
                self.alerting_list.append(alert)
            elif alert.alert_state == AlertState.NODATA:
                self.nodata_list.append(alert)
            else:
                self.error_list.append(alert)

    def count_alerts_in_group(self, alert_group_message:str):
        """Counts the number of alerts present in an alert group"""
        subtring = "Alert Summary"
        count = alert_group_message.count(subtring)
        return count

    async def send_message_in_groups(self, alert_group_messages=None):
        """Sends all messages in an alert_group"""
        if alert_group_messages is None:
            alert_group_messages = self.alert_group_messages
        
        for alert_group in alert_group_messages.keys():
            title = f"Alert Group: {alert_group}\n\n"
            count = self.count_alerts_in_group(alert_group_messages[alert_group])
            header = f"Number of alerts: {count}\n\n"
            await self.send_alert(title + header + alert_group_messages[alert_group])
    
    async def send_alert(self, message):
        """Helper function to send one alert via telegram"""
        tele_client = TelegramService()
        tele_client.retrieve_token_from_environment()
        await tele_client.send_telegram_message(message)

