# RP Urban Farm Custom Alerting System

# Dependencies
1. ``pip install pandas``

## Alerts Created

### Grow Light On Alert & Grow Light Off Alert
The alerting system for the grow lights operates based on the principle that alerts should be triggered only when the grow lights are first switched on or first switched off, rather than continuously throughout their operation hours. This approach reduces unnecessary noise and spamming of alerts. To determine the state of the grow lights, the system compares the difference in power consumption between two consecutive data points. Let's consider the grow light's operation hours from **0700hrs to 1900hrs** as an example.
* Between 0600hrs and 0700hrs: The power consumption difference will be significant, for example, +370W, as the grow lights transition from the OFF state to the ON state.
* Between 0700hrs and 1900hrs: The power consumption difference will be small, typically less than or equal to +5W, as the grow lights remain in the ON state.
* Between 1900hrs and 2000hrs: The power consumption difference will again be significant, for example, -370W, as the grow lights transition from the ON state to the OFF state.
* Between 2000hrs and 0600hrs: The power consumption difference will be insignificant, typically less than or equal to +5W, as the grow lights remain in the OFF state.

 A buffer of +-30W was used to obtain threshold values to determine when each rack is switched on or off. Change in power consumption for each rack were observed to be: 
* Rack 1 +370W (ON), -370W (OFF)
* Rack 2 +340W (ON), -340W (OFF) 
* Rack 3 +270W (ON), -270W (OFF)

## Data Gap Alerts
A data gap refers to the absence of a data point in our InfluxDB server. There can be various reasons for data gaps, such as sensor disconnection, network instability, or API timeouts. To ensure the effectiveness of recovery mechanisms like automatic network reconnect, we have set up Data Gap alerts. These alerts notify us whenever the data gap exceeds a specified threshold (**default: 0.3**) i.e., 30%. 

The alert mechanism works by retrieving all the data points within a specified time range (**default: 6 hours**) from the database. An aggregation operation is then performed with a specified interval (**default: 30 minutes**), and the *createEmpty* parameter is set to true. This ensures that missing time points are populated with **none** values.

During the processing of the query result, the data is read into a dataframe, and the **none** values are transformed into **NaN** (Not a Number) values. The number of NaN fields is then compared to the total number of fields retrieved to calculate the data gap percentage. This percentage is evaluated against the data gap threshold to determine whether an alert needs to be sent out.

### Validating Data Gap Alerts
* [0% Data Gap Threshold](alerts_validation/data_gap_alerts_threshold-0.txt): In this scenario, threshold was set to 0% i.e., strictly no data gaps allowed. Since the evaluation does a greater than or equal to comparison, all alerts will be set to AlertState.ALERTING, and telegram alert will be sent.
* [30% Data Gap Threshold](alerts_validation/data_gap_alerts_threshold-30.txt):In this scenario, threshold was set to 30%. Since all buckets do not have data gaps that exceed 30%, AlertState will be set to AlertState.OK and no alerts will be sent out. 

# CRON Expression
The ``scheduled_growlight_alerts.py``, was configured to be evaluated at the 5th minute of every hour. This 5 minute buffer was incorporated to ensure sensors would have enough time to write new data to database i.e., network latency buffer.
* ``5 * * * * cd /home/yappi/ITP-SE12-Power-Monitoring/alerts && python3 scheduled_growlight_alerts.py >> /home/yappi/ITP-SE12-Power-Monitoring/alerts/output.txt`` 

The ``scheduled_data_gap_alerts.py`` was configured to be evaluated every 6 hours. 
* ``** */6 * * * cd /home/yappi/ITP-SE12-Power-Monitoring/alerts && python3 scheduled_data_gap_alerts.py >> /home/yappi/ITP-SE12-Power-Monitoring/alerts/data_gap_output.txt``