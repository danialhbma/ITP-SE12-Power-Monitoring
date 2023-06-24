# InfluxDB 

## Mass create buckets
1. Add bucket name and description to buckets.json
2. python3 BucketCreator.py 
	* Buckets that already exists will be ignored, buckets that do not exist will be created.

## Write Data To InfluxDB Server Using Python
Writing to InfluxDB involves two classes, InfluxDBWriter and InfluxDBMeasurement (Abstract). InfluxDBMeasurement is an abstract class to be
inherited, the _set_tags() and _set_fields() function must be implemented by sub-classes. See OpenWeatherMapAPIClient.py and code comments for example usage.
* Tags are used for filtering e.g., device name.
* Fields are actual data / values e.g., Temp, Humidity etc.
* Tags and Fields are used to create a Point object (Measurement). 
* InfluxDBWriter.write_single_measurement() takes in a Point object, and writes this point object to InfluxDB server.

## OpenWeatherMapAPI
Retrieves weather information from OpenWeatherMapAPI. Weather information is then written to InfluxDB server. This script will be scheduled via a CRON job and executed every 30 minutes. 
1. In OpenWeatherMapAPIClient, verify valid API, longitude and latitude used.
2. In InfluxDBWriter.py, verify valid API token, org and URL used. 
3. pip3 install influxdb-client
4. python3 OpenWeatherMapAPIClient.py	

## Creating CRON Jobs
Cron is a time-based job scheduling system in Unix-like operating systems. It allows users to schedule and automate the execution of commands or scripts at specific intervals or times. Cron jobs are defined using a specific syntax known as cron expressions.
1. crontab -e
	* To schedule a CRON job that executes a script every 30 minutes, you can use the following CRON expression.
	* */30 * * * * cd < path to folder containing script > && python3 < script name > 
	* e.g., */30 * * * *  cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && python3 OpenWeatherMapAPIClient.py  >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/output.log 2>&1
	* The expression above also redirects the output from OpenWeatherMapAPIClient.py to output.log, this is mainly for debugging and is not mandatory. 
2. crontab -l 
	* View CRON jobs scheduled	

# InfluxDB Backups & Restore
Use the influx backup command to back up data and metadata stored in InfluxDB. InfluxDB copies all data and metadata to a set of files stored in a specified directory on your local filesystem.
1. cd into InfluxDB docker image shell
	* sudo docker exec -it <container id> /bin/bash
	* e.g., docker exec -it 85467b4a3382 /bin/bash
2. influx backup <path_to_backup>
	* stores backup files (tar.gz) in the specified path
3. influx restore <path_to_backup>

## Manually Trigger InfluxDB Backup
The influx_db_backup.sh bash script is used to create an InfluxDB backup. 
* You can manually trigger a backup by running the bash script ./influx_db_backup.sh
* InfluxDB backups exists as tar.gz files, and can be used to restore a database.
* The bash script will also copy the backup files into the InfluxDB directory. Easier way to access and view / analyze files as required. 

## Automatic Scheduling of Backups
As of writing a backup of the InfluxDB database is created every Sunday at 23:59 (SG Time). This is achieved by scheduling a CRONJOB using the expression below 
* 59 23 * * 0 ./influx_db_backup.sh
* e.g, 59 23  * * 0 cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && sudo ./influx_db_backup.sh >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/backup-logs.txt 2>&1

