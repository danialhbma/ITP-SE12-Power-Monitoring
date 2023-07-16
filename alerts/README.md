# RP Urban Farm Custom Alerting System

# Dependencies
1. ``pip install pandas``

## Alerts Created

### 1. Grow Light On Alert & Grow Light Off Alert
The alerting system for the grow lights operates based on the principle that alerts should be triggered only when the grow lights are first switched on or first switched off, rather than continuously throughout their operation hours. This approach reduces unnecessary noise and spamming of alerts. To determine the state of the grow lights, the system compares the difference in power consumption between two consecutive data points. Let's consider the grow light's operation hours from **0700hrs to 1900hrs** as an example.
* Between 0600hrs and 0700hrs: The power consumption difference will be significant, for example, +370W, as the grow lights transition from the OFF state to the ON state.
* Between 0700hrs and 1900hrs: The power consumption difference will be small, typically less than or equal to +5W, as the grow lights remain in the ON state.
* Between 1900hrs and 2000hrs: The power consumption difference will again be significant, for example, -370W, as the grow lights transition from the ON state to the OFF state.
* Between 2000hrs and 0600hrs: The power consumption difference will be insignificant, typically less than or equal to +5W, as the grow lights remain in the OFF state.

 A buffer of +-30W was used to obtain threshold values to determine when each rack is switched on or off. Change in power consumption for each rack were observed to be: 
* Rack 1 +370W (ON), -370W (OFF)
* Rack 2 +340W (ON), -340W (OFF) 
* Rack 3 +270W (ON), -270W (OFF)

## Extended NODATA Alerts
Hardware configuration may be prone to unintended failures. Recovery mechanisms can be set in place i.e., handling network timeouts or connection issues. However, it is often impractical or impossible for sensors to continously work for extendeed periods without encountering issues. 

# CRON Expression
The ``scheduled_growlight_alerts.py``, was configured to be evaluated at the 5th minute of every hour. This 5 minute buffer was incorporated to ensure sensors would have enough time to write new data to database i.e., network latency buffer.
* ``5 * * * * cd /home/yappi/ITP-SE12-Power-Monitoring/alerts && python3 scheduled_growlight_alerts.py >> /home/yappi/ITP-SE12-Power-Monitoring/alerts/output.txt`` 
