from TelegramAlertModule import *
from DateRangeManager import DateRangeManager 
import pandas as pd 

class GrowlightOffAlert(Alert):
    def __init__(self, alert_id, threshold:int, measurement_name):
        # Alert used to determine time when growlight was switched o
        super().__init__(alert_id=alert_id, evaluation_interval="1h", alert_group="Grow Light Off Alert")
        self.threshold = threshold 
        self.measurement_name = measurement_name
        self.growlight_switched_off_query()
        self.drm = DateRangeManager()

    def _evaluate_alert(self, wattage) -> AlertState:
        """ Sets the alert state based on wattage difference received 
            e.g, if wattage difference >= -390 W, growlight recently switched off -> send on alert
            if wattage difference ~ 0.98, no change in growlight state i.e., ON-ON-ON, off-off-off, no need to send alert
        """
        if (wattage is None):
            return AlertState.NODATA
        try:
            # If wattage is within +-30 of threshold, set it to alerting state
            if wattage > 30: # If wattage difference reading > 30, can guarantee that switch did not just turn off, hence can ignore
                return AlertState.OK
            if (self.threshold - 30 <= wattage <= self.threshold + 30): # add a +-30 W buffer
                return AlertState.ALERTING
            else: 
                return AlertState.OK
            return AlertState.ERROR # Unknown state
        except TypeError as e:
            raise TypeError(f"Inappropriate threshold: [{self.threshold}] or wattage [{wattage}] provided")

    def _process_query_results(self, query_result):
        # Processes query results to extract wattage needed to perform threshold analysis
        try:
            df_handler = InfluxDBDataFrameHandler()
            df = df_handler.format_as_dataframe(query_result)
            value, time, *ignore = df_handler.get_value_and_formatted_time(df)[0]
            sg_time = self.drm.utc_to_sg_time(time)
            return value, sg_time
        except ValueError as e:
            raise ValueError(f"No data found: {e}")

    def growlight_switched_off_query(self):
        """ 
            Retrieves the difference in wattage between the last two data points.
            Query is designed to capture large delta difference when growlight is initally switched on or off.
            When growlight was just turned on difference between points will be = 390W. 
            When growlight was just turned off difference between points will be  -390W.
            During growlight operation hours, power consumption stays constant at 390W, hence the difference between '
            two points will be around 0.98 and will not meet threshold.
            Similarly when growlight is not operating, power consumptions stays at ~0.98 to 1, hence difference between
            points will not meet threshold. 
            This query allows alerts to be sent ONLY WHEN growlight is first turned on or off.
        """
        date_range_manager = DateRangeManager()
        start, end = date_range_manager.get_time_range("2h")
        query = f'''from(bucket: "Power Consumption")
                |> range(start: {start}, stop: {end})
                |> filter(fn: (r) => r["_measurement"] == "{self.measurement_name}")
                |> aggregateWindow(every: 1h, fn: mean, createEmpty: true)
                |> fill(column: "_value", usePrevious: true)
                |> map(fn: (r) => ({{ r with _value: if exists r["_value"] then r["_value"] else 0.0 }}))
                |> difference(columns: ["_value"], keepFirst: false)
                |> first()
                '''
        """
        query = f'''from(bucket: "Power Consumption")
            |> range(start: {start}, stop:{end})
            |> filter(fn: (r) => r["_measurement"] == "{self.measurement_name}")
            |> aggregateWindow(every: 1h, fn:mean, createEmpty: true)  
            |> fill(column: "_value", usePrevious: true)
            |> difference(columns: ["_value"], keepFirst:false)
            |> first()
            '''
        """
        self.set_alert_query(query)


    def _create_alert_message(self, alert_state: AlertState, time, exception=""):
        # Creates alert message object
        alert_message = GrowlightOffAlertMessage(self.alert_id, self.measurement_name)
        alert_message.format_message(alert_state, time, exception)
        return alert_message

    def evaluation(self, query_result):
        """Inherited function, performs alert evaluation and creates alert message"""
        try: 
            wattage, time = self._process_query_results(query_result)
            self.update_alert_state(self._evaluate_alert(wattage)) # Determines if wattage is above threshold
            self.alert_message = self._create_alert_message(self.alert_state, time)
        except ValueError as e:
            time = self.drm.current_sg_time()
            self.update_alert_state(AlertState.NODATA)
            self.alert_message = self._create_alert_message(self.alert_state, time, exception=str(e))
        except TypeError as e:
            self.update_alert_state(AlertState.ERROR)
            time = self.drm.current_sg_time()
            self.alert_message = self._create_alert_message(self.alert_state, time, exception=str(e))

class GrowlightOffAlertMessage(AlertMessage):
    def __init__(self, alert_id, measurement_name):
        super().__init__(message_id=f"{alert_id}")
        self.location = self._format_measurement_name(measurement_name)
        
    def _format_measurement_name(self, measurement_name):
        # Formats Rack_1_Light into Rack 1 Growlight
        parts = measurement_name.split("_")  # Split the string at underscores
        rack_number = parts[1]  # Extract the rack number
        return f"Rack {rack_number} Growlight"

    def _populate_message_elements(self, alert_state: AlertState, time, exception = ""):
        """Populate AlertMessage summary and description"""
        if alert_state == AlertState.OK:
            # No need to format message since alert does not need to be fired
            self.summary += f"{self.message_id} - OK"
            self.description += f"Alert will only fire when growlight is first switched on or first switched off."
            return 

        if alert_state == AlertState.ERROR:
            self.summary += f"Encountered error while executing - [{self.message_id}]."
            self.description += f"Contact administrators if this is a recurring issue.\nException caught:{exception}"
            return 

        if alert_state == AlertState.ALERTING:
            self.summary += f"{self.location} switched off."
            self.description += f"{self.location} switched off at {time}."
            return 

        if alert_state == AlertState.NODATA:
            self.summary += f"Unable to retrieve data from {self.location}"
            self.description += f"Failed to retrieve growlight power consumption from {self.location} at {time}."
            return
    
    def format_message(self, alert_state, time, exception = "") -> str: 
        """Formats the Growlight On alert message based on how message elements were populated"""
        self._populate_message_elements(alert_state, time)
        self.message = f"{self.summary}\n{self.description}"

