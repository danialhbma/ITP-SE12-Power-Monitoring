from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
import pandas as pd  

class DataGapAlert(Alert):
    """
    DataGapAlert is activated when one or more measurements within an InfluxDB bucket show data gaps that exceed a predefined threshold.
    
    Args:
        alert_id (str): The identifier for the alert.
        threshold_percent (float): The data gap threshold expressed as a percentage. Default is 0.3, indicating that more than 30% missing data in the measurement will trigger the alert.
        bucket_name (str): The name of the InfluxDB bucket where the measurements are stored.
        evaluation_interval (str, optional): The time window used for the query to assess data gaps. Defaults to "6h".
        aggregate_window_interval (str, optional): The window period over which the data is aggregated for analysis. Defaults to "30m".
    """
    def __init__(self, alert_id: str, bucket_name: str, data_gap_threshold: float = 0.3, evaluation_interval: str = "6h", aggregate_window_interval: str = "30m"):
        super().__init__(alert_id, evaluation_interval=evaluation_interval, alert_group=alert_id)
        self.alert_threshold = data_gap_threshold  # Threshold for data gap percentage
        self.bucket_name = bucket_name
        self.aggregate_window_interval = aggregate_window_interval
        self.measurements_data_gap_rate = {} # {measurement_name} : {data gap %}
        self.create_alert_query()
        self.measurements_affected = [] # maintains a list of measurements that exceed data gap threshold

    def _process_query_results(self, query_result):
        """Updates measurements integrity dictionary, each measurement will have their data integrity assessed in evaluation"""
        df_handler = InfluxDBDataFrameHandler()
        # Format query result as dataframe
        df = df_handler.format_as_dataframe(query_result)
        if df.empty:
            raise ValueError(f"Dataframe is Empty. Check query: {self.alert_query}")

        # Retrieve list of measurements in bucket
        measurements = df['_measurement'].unique()
        for measurement in measurements:
            if measurement == "Rack_3_Light" or measurement == "Rack_3_Water":
                # Rack_3_Light uses the small tuya socket which only sends data when there are changes in power consumption.
                # Excluded from data gap analysis. 
                continue
            filtered_df = df.loc[df['_measurement'] == measurement]
            # Exclude the last entry - last entry is automatically created since aggregation operation
            filtered_df = filtered_df.iloc[:-1]
            print(filtered_df)
            total_count = len(filtered_df) # Number of entries within window (NaN included)
            not_null_count = filtered_df['_value'].count() # Number of entries excluding NaN
            data_gap = ((total_count - not_null_count) / total_count) # % of loss data
            self.measurements_data_gap_rate[measurement] = data_gap    

    def evaluation(self, query_result):
        """Processes query results and updates the alert state following alert evalution."""
        drm = DateRangeManager()
        time = drm.current_sg_time()
        try:
            self._process_query_results(query_result)
            self.update_alert_state(self._evaluate_alert()) 
            self.alert_message = self._create_alert_message(self.alert_state, time)
        except Exception as e:
            self.update_alert_state(AlertState.NODATA)
            self.alert_message = self._create_alert_message(self.alert_state, time, exception=e)
            print(f"Encountered error while during evaluation: {e}")

    def _evaluate_alert(self) -> AlertState:
        """
        Iterates through the measurements data gap dictionary to determine if any buckets have data gaps that exceed threshold.
        If a measurement is found to have exceeded data gap threshold, AlertState.ALERTING will be returned i.e., need to send telegram alerts.
        If all measurements do not exceed data gap threshold, no need to send alerts hence return AlertState.OK
        """
        try: 
            if not self.measurements_data_gap_rate:
                # If dictionary is empty, query most likely returned empty values
                return AlertState.NODATA
        
            for measurement in self.measurements_data_gap_rate.keys():
                if self.measurements_data_gap_rate[measurement] >= self.alert_threshold:
                    # If threshold exceeded, update count and affected
                    self.measurements_affected.append(measurement)
            return AlertState.OK if len(self.measurements_affected) == 0 else AlertState.ALERTING
        except Exception as e:
            # Unexepected error occured
            print(f"Encountered error while trying to evaluate alert: {str(e)}")
            return AlertState.ERROR

    def _create_alert_message(self, alert_state: AlertState, time, exception="") -> AlertMessage:
        # Create an alert message with the data gap information
        alert_message = DataGapAlertMessage(self.alert_id, self.bucket_name, self.alert_threshold, self.measurements_affected)
        alert_message.format_message(alert_state, time, exception)
        return alert_message

    def create_alert_query(self):
        # Create the query to retrieve the data for evaluation
        drm = DateRangeManager()
        start, stop = drm.get_time_range(self.evaluation_interval)
        query = f'''
        from(bucket: "{self.bucket_name}")
            |> range(start: {start}, stop: {stop})
            |> filter(fn: (r) => r["_measurement"] != "" and r["_field"] != "weather_main")
            |> window(every: {self.aggregate_window_interval}, createEmpty: true)
        '''
        self.set_alert_query(query)

class DataGapAlertMessage(AlertMessage):
    def __init__(self, alert_id:str, bucket_name:str, alert_threshold:float, measurements_affected:list = []):
        super().__init__(message_id=f"{alert_id}")
        self.bucket_name = bucket_name
        self.threshold = alert_threshold
        self.message = ""
        self.measurements_affected = measurements_affected
        
    def _populate_message_elements(self, alert_state: AlertState, time, exception = ""):
        """Populate AlertMessage summary and description"""
        if alert_state == AlertState.OK:
            self.summary += f"No major data gaps present in: {self.bucket_name}."
            self.description += f"Data gaps in {self.bucket_name} do not exceed threshold of: {self.threshold * 100}%"

        elif alert_state == AlertState.ALERTING:
            self.summary += f"Data gaps detected in {self.bucket_name} bucket.\nData gaps present in a total of: {len( self.measurements_affected )} measurement(s)"
            self.description += f"Measurement(s) with data gaps that exceeds threshold of {self.threshold * 100}%:\n"
            for index, measurement in enumerate(self.measurements_affected, start=1):
                self.description += f"({index}) {measurement}\n"

        elif alert_state == AlertState.NODATA:
            self.summary += f"Unable to retrieve data from {self.measurement_name}"
            self.description += f"Failed to retrieve data from {self.measurement_name} at {time}."

        else:
            self.summary += f"Encountered error while executing - [{self.message_id}]."
            self.description += f"Contact administrators if this is a recurring issue.\nException caught:{exception}"
          
    def format_message(self, alert_state, time, exception = ""): 
        """Formats the DataGap alert message"""
        self._populate_message_elements(alert_state, time)
        self.message = f"{self.summary}\n{self.description}"

