from TelegramAlertModule import * 
from DateRangeManager import DateRangeManager 
import pandas as pd 

class DataGapAlert(Alert):
    """
    DataGapAlert is triggered if bucket contains X or more missing data points in a X-hour window.
    """
    def __init__(self,alert_id:str, window_interval:str, missing_data_threshold:int, evaluation_interval:str="30m"):
        super().__init__(alert_id=alert_id, evaluation_interval = evaluation_interval, alert_group="Data Gap Alert") # init parent alert
        self.dead_interval = declare_dead_interval # How many hours of failed sending before sensor is considered dead
        self.bucket_name = bucket_name
        self.missing_data_threshold = missing_data_threshold
        self.window_interval = window_interval

    def _evaluate_alert(self, missing_data_count:int):
        if (missing_data_count is None):
            return AlertState.NODATA
        try:
            if missing_data_count == 0 or missing_data_count < self.missing_data_threshold:
                return AlertState.OK
            elif missing_data_count >= self.missing_data_threshold:
                return AlertState.ALERTING
            return AlertState.ERROR # Unknown state
        except TypeError as e:
            raise TypeError(f"Inappropriate threshold: Please ensure [{self.missing_data_threshold}] and [{missing_data_count}] are valid integers")

    def evaluation(self, query_result):
        """Business logic evaluate queries"""
        pass

    def _create_alert_message(self):
        pass
    
class DataGapAlertMessage(AlertMessage):
    def __init__(self):
        pass 
    
    def format_message(self):
        pass
    
