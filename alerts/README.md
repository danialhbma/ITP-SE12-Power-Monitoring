#Alerts

#Dependencies
1. ``pip install pandas``

#CRON Expression
The ``scheduled_growlight_alerts.py``, was configured to be evaluated at the 5th minute of every hour.
``5 * * * * cd /home/yappi/ITP-SE12-Power-Monitoring/alerts && python3 scheduled_growlight_alerts.py >> /home/yappi/ITP-SE12-Power-Monitoring/alerts/output.txt`` 
