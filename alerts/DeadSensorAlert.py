from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
import pandas as pd  
from datetime import datetime

class DeadSensorAlert(Alert):
    def __init__(self, alert_id:str, bucket_name:str, alert_evaluation_group:str="Dead Sensor Alert", threshold:str="6h"):
        """
        This alert monitors all measurements in a specific InfluxDB bucket, keeping track of the timestamps of their most recent data points.
        An alert is issued if the latest data point of a measurement is older than the specified threshold. 
        Hence, a sensor is classified as 'dead' if it hasn't transmitted any data within the defined threshold period.
        """
        super().__init__(alert_id=alert_id, evaluation_interval="6h", alert_group=alert_evaluation_group)
        self.bucket_name = bucket_name
        self.create_alert_query()

        self.threshold = threshold # threshold for when an alert should be sent
        self.drm = DateRangeManager()
        self.expected_latest_data_time = self.drm.get_time_minus_window(self.threshold) # latest data point in InfluxDb must be greater than this expected_latest_data_time, else sensor will be deemed as dead.

        self.latest_data_points = {} # Contains last data point received for all measurements in bucket - {measurement_name: date}
        self.dead_sensors = {}

    def create_alert_query(self) -> str:
        """Returns the last measurement received in bucket."""
        query = f'''
        from(bucket: "{self.bucket_name}")
        |> range(start: -365d)
        |> filter(fn: (r) => r["_measurement"] != "" and r["_field"] != "weather_main")
        |> group(columns: ["_measurement"], mode:"by")  
        |> last()  
        '''
        self.set_alert_query(query)

    def evaluation(self, query_result):
        """
        Determines if all measurements in a bucket has a data point that is after the expected latest data point timestamp.
        Creates the appropriate alert messages.
        """
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

    def _process_query_results(self, query_result):
        """Formats query results into a data frame, returns measurement name and last date (utc time) of data point received as a dictionary"""
        df_handler = InfluxDBDataFrameHandler()
        df = df_handler.format_as_dataframe(query_result) # format query result as dataframe

        if df.empty:
            raise ValueError(f"Dataframe is Empty. Check query: {self.alert_query}")
        
        for index, row in df.iterrows():
            # Extract the '_time' and '_measurement' values from each row
            utc_time =  row['_time']
            measurement = row['_measurement']
            
            # Add the values to the dictionary with offset-naive timestamps
            self.latest_data_points[measurement] = utc_time

    def _evaluate_alert(self) -> AlertState:
        """Checks if the last data points for all measurements exceed the threshold time."""
        try:
            # Return NODATA state if dictionary is empty
            if not self.latest_data_points:
                return AlertState.NODATA

            # Check if the last data point for each measurment, occured after the expected latest data time (threshold)
            for measurement in self.latest_data_points.keys():
                sensor_alive = self.latest_data_points[measurement] > self.expected_latest_data_time
                if not sensor_alive: # Sensors are deemed to be dead, if their last sent data is before the expected latest data time
                    self.dead_sensors[measurement] = self.drm.utc_to_sg_time(self.latest_data_points[measurement])

            if not self.dead_sensors: # If dead_sensors is empty, dont need to send alerts, all OK
               return AlertState.OK
            else:  # If dead_sensors is not empty, one or more measurements has a dead sensor, send alert
                return AlertState.ALERTING 

        except Exception as e:
            print(f"Unexpected error encountered while trying to evaluate alert: {str(e)}")
            return AlertState.ERROR
    
    def _create_alert_message(self, alert_state, time, exception="") -> AlertMessage:
        """Creates the DeadSensorAlertMessage"""
        alert_message = DeadSensorAlertMessage(self.alert_id, self.bucket_name, self.dead_sensors, self.expected_latest_data_time)
        alert_message.format_message(alert_state, time, exception)
        return alert_message

class DeadSensorAlertMessage(AlertMessage):
    def __init__(self, alert_id:str, bucket_name:str, dead_sensors:dict, expected_latest_data_time):
        super().__init__(message_id=f"{alert_id}")
        self.bucket_name = bucket_name
        self.message = ""
        self.measurements_affected = dead_sensors
        self.expected_latest_data_time = expected_latest_data_time

    def _populate_message_elements(self, alert_state: AlertState, time, exception = ""):
        """Populate AlertMessage summary and description"""
        if alert_state == AlertState.OK:
            self.summary += f"Sensors used to update {self.bucket_name} are working as intended."
            self.description += f"All measurements in {self.bucket_name} have data points sent after {self.expected_latest_data_time}"

        elif alert_state == AlertState.ALERTING:
            self.summary += f"Sensors failed to send data to - {self.bucket_name} bucket."
            self.description += f"Please check the status of the sensors for the following measurement(s):\n"

            # Enumerating affected measurements
            for index, measurement in enumerate(self.measurements_affected.keys(), start=1):
                self.description += f"({index}) {measurement}: Last data received at {self.measurements_affected[measurement]}\n"

        elif alert_state == AlertState.NODATA:
            self.summary += f"Unable to retrieve data from {self.measurement_name}"
            self.description += f"Failed to retrieve data from {self.measurement_name} at {time}."

        else:
            self.summary += f"Encountered error while executing - [{self.message_id}]."
            self.description += f"Contact administrators if this is a recurring issue.\n Exception caught:{exception}"
          
    def format_message(self, alert_state, time, exception = ""): 
        """Formats the DataGap alert message"""
        self._populate_message_elements(alert_state, time)
        self.message = f"{self.summary}\n{self.description}"
