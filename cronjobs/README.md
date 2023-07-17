# CRON Jobs
Cron jobs are scheduled tasks that can be automatically executed at predefined intervals on Unix-like operating systems, including Linux and macOS. These tasks are controlled by the cron daemon, a background process that runs continuously and checks for scheduled jobs to execute.

Cron jobs are often used for automating routine tasks, such as system maintenance, backups, log rotation, and running scripts or commands. They provide a convenient way to perform repetitive actions without requiring manual intervention.

# Creating CRON Jobs
To create a cron job, you need to use the crontab command, which allows you to manage the cron table—a file that contains the list of scheduled jobs. Each user on a system can have their own cron table.

Here's how you can create a new cron job:
1. Open a terminal or shell session.
2. Type ``crontab -e`` to open the cron table in the default editor.
3. If prompted, choose an editor (e.g., nano, vim, or emacs) to edit the cron table.
4. In the editor, add a new line for your cron job using the appropriate syntax.
5. Save the file and exit the editor.
6. ``crontab -l`` can be used to view the list of scheduled cron jobs.

## CRON Expressions Quick Guide
Cron expressions are used to schedule tasks, known as cron jobs, on Unix-like operating systems. They consist of five fields separated by spaces, representing different time intervals. Refer to the section below to understand what time interval each field represents. 
* `` * * * * * [path to script]``
* If you are having trouble coming up with cron expressions you can use this cron expression generator - https://crontab.guru/#59_23_*_*

## Understanding CRON Expression Time Intervals 
Minute: The minute(s) when the job should run (0-59).
Hour: The hour(s) when the job should run (0-23).
Day of the Month: The day(s) of the month when the job should run (1-31).
Month: The month(s) when the job should run (1-12).
Day of the Week: The day(s) of the week when the job should run (0-6, 0-Monday, 6-Sunday).

Examples:
1. Run job every minute: ``* * * * * hello_world.py``
2. Run job at the beginning of every hour: ``* * * * * hello_world.py``
3. Run job at the 30th minute of every hour: ``*/30 * * * * hello_world.py``
4. Run job daily at 2359: ``59 23  * * * hello_world.py``

# Scheduled Cron Jobs
The **crontab.txt** file provided contains the list of all scheduled cron jobs used in this project. Instead of providing the actual script itself, we are providing commands to change directory to location containing script before executing the script. This was done to as certain scripts require loading of environmental variables within the **.env** file that resides in the corresponding directory. We also redirected all outputs to an output file for debugging. Redirecting of output is not necessary but recommended as it facilitates debugging.

## Retrieving External Weather Conditions from OpenWeatherMap 
The [OpenWeatherMapAPIClient](../InfluxDB/OpenWeatherMapAPIClient.py) was designed to query OpenWeatherMapAPI to retrieve external weather conditions. We scheduled an API call to be made every 30 minutes using the CRON expression below. 
* ``*/30 * * * *  cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && python3 OpenWeatherMapAPIClient.py >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/output.log 2>&1``

## Automating InfluxDB Backups
The [influx_db_backup](../InfluxDB/influx_db_backup.sh) bash script automates retrieval of InfluxDB backups by entering the shell of the docker image and running the backup command. It also copies all backups to [influxdb_backups](../InfluxDB/influxdb_backups) folder for easier retrieval. This script was scheduled to run daily at 2359 using the CRON expression below.
* ``59 23  * * * cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && sudo ./influx_db_backup.sh >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/influxdb_backups/backup-logs.txt 2>&1``

## Automating Docker Logs Retrieval
The [generate_docker_logs](../docker-containers/docker_logs/generate_docker_logs.py) script automates retrieval of the 1000 most recent docker logs. Docker logs are helpful when doing debugging or system investigations. Log files can be found [here](../docker-containers/docker_logs). This script was scheduled to run daily at 2359 using the CRON expression below. 
* ``59 23 * * * cd /home/yappi/ITP-SE12-Power-Monitoring/docker-containers/docker_logs && python3 generate_docker_logs.py  >> /home/yappi/ITP-SE12-Power-Monitoring/docker-containers/docker_logs/output.txt``

## System Monitoring
System monitoring plays a vital role in cloud deployments, ensuring the health and performance of the system. The Google Cloud Console Platform (GCP) offers powerful logging and monitoring capabilities. However, these features come with a cost and can only be accessed through the GCP dashboard. To address this, we have developed our own  [System Monitoring Agent](../telegram_service/SystemMonitoringAgent.py) This agent is designed to monitor various system metrics such as remaining disk space, network usage, and RAM usage. When any of the monitored metrics exceed a predefined threshold, such as memory usage surpassing 80%, an alert is sent via Telegram to notify the relevant parties. Conversely, if all system health checks pass successfully, a system health OK message is dispatched. By leveraging our custom monitoring agent, we gain flexibility and control over the monitoring process, enabling us to proactively manage and address potential issues in our system. This script was scheduled to run daily at 2359 using the CRON expression below.
* ``59 23 * * * cd /home/yappi/ITP-SE12-Power-Monitoring/telegram_service && python3 SystemMonitoringAgent.py >> monitoring_reports.txt 2>&1``

## Threshold Analysis & Telegram Alerts
Grafana was configured to detect and alert abnormal conditions such as high temperature, high CO2 levels, and disrupted water flow rates. However, we encountered difficulties when setting up alerts to notify whenever the grow lights switched on or off. To overcome this challenge, we developed our own Python-based solution called [Telegram Alert Module](../alerts/TelegramAlertModule.py). This module offers a customized alert system that integrates with our existing infrastructure. It utilizes several key components, including our custom [InfluxDB Reader](../InfluxDB/InfluxDBReader.py), [DateRangeManager](../InfluxDB/DateRangeManager.py) and [DataFrameHandler](../InfluxDB/InfluxDBDataFrameHandler.py) classes to directly query InfluxDB database, to retrieve data stored and to perform threshold analysis. It also uses [TelegramService](../telegram_service/TelegramService.py) to send out telegram alerts. 

###  Grow light Alerts 
Grow light alerts were scheduled to run at the 5th minute of every hour using the CRON exrpession below. 
* ``5 * * * * cd /home/yappi/ITP-SE12-Power-Monitoring/alerts && python3 scheduled_growlight_alerts.py >> /home/yappi/ITP-SE12-Power-Monitoring/alerts/output.txt``
