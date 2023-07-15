# InfluxDB 
This directory contains helper classes and functions used to interact with InfluxDB Server.

## Mass create buckets
1. Add bucket name and description to buckets.json
2. ``python mass_create_buckets.py``
	* Buckets that already exists will be ignored, buckets that do not exist will be created.

## Write Data To InfluxDB Server Using Python
To write data to an InfluxDB server using Python, you can utilize the ``InfluxDBWriter.py`` and ``InfluxDBMeasurement.py`` (abstract) classes. The **InfluxDBMeasurement** class serves as an interface or blueprint for creating measurements to be written to InfluxDB. It is an abstract class that requires subclasses to implement its **_set_tags()** and **_set_fields()** functions. 
* Tags are used for filtering e.g., device name.
* Fields are actual data / values e.g., Temp, Humidity etc.
* Tags and Fields are used to create a Point object (Measurement). 
* InfluxDBWriter.write_single_measurement() takes in a Point object, and writes this point object to InfluxDB server.
* See OpenWeatherMapAPIClient.py or Sensors.py for example usage. 
* The ``influx_db_write_test.py`` script is used to verify writes to InfluxDB server. Modify the InfluxDB URL, api key and token as required. By default, it creates and writes simulated data to *Sensors (Testing)* bucket.  

## Read Data From InfluxDB Server using Python
To write data to an InfluxDB server using Python, you can use ``InfluxDBReader.py``. This class serves as a Read Gateway to InfluxDB buckets. It allows retrieval of data from specified buckets, data can be transformed and loaded into *pandas dataframe* or exported to a csv file for downstream manipulation.
* ``DateRangeManager.py`` is a helper class that manages influx query date ranges. It performs data validation and creation.
* To execute a read query using **InfluxDBReader** class:
	1. ``from InfluxDBReader import InfluxDBReader``
	2. ``reader = InfluxDBReader(URL, INFLUXDB_TOKEN, INFLUXDB_ORG)``
	3. ``bucket_data = reader.read_from_bucket(bucket_name, time_window, aggregate_window_interval)``
		* **time_window** is the time window for querying the data. It follows the format {length}{unit}, where length is an integer greater than 0 and unit can be one of the following: "s" (seconds), "m" (minutes), "h" (hours), "d" (days), "w" (weeks).
		* **aggregate_window_interval** is an optional parameter to specify the interval for aggregating the data. The default is "30m" (30 minutes).
		* Examples of valid time_window and aggregate_window_intervals include: "30s" (30 seconds), "1h" (1 hour) etc.
		* e.g., ``bucket_data = reader.read.from_bucket(Power Consumption, "30d", "1h")``, This query retrieves all measurements from the "Power Consumption" bucket for the past 30 days, and aggregates the data based on a 1-hour window.
	4. The returned bucket_data will contain the queried data in the form of a FluxTable (list of tables). You can then further process the data by converting it into a pandas DataFrame using the **query_result_to_dataframe** method or export it to a CSV file using the **dataframe_to_csv** method of the InfluxDBReader class.
* For code usage example see ``extract_raw_data.py``. 

## OpenWeatherMapAPIClient
Retrieves weather information from OpenWeatherMapAPI. Weather information is then written to InfluxDB server. This script will be scheduled via a CRON job and executed every 30 minutes. 
1. In OpenWeatherMapAPIClient, verify valid API, longitude and latitude used.
2. In InfluxDBWriter.py, verify valid API token, org and URL used. 
3. ``pip3 install influxdb-client``
4. ``python3 OpenWeatherMapAPIClient.py``

## Creating CRON Jobs
Cron is a time-based job scheduling system in Unix-like operating systems. It allows users to schedule and automate the execution of commands or scripts at specific intervals or times. Cron jobs are defined using a specific syntax known as cron expressions.
1. crontab -e
	* To schedule a CRON job that executes a script every 30 minutes, you can use the following CRON expression.
	* */30 * * * * cd < path to folder containing script > && python3 < script name > 
	* e.g., ``*/30 * * * *  cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && python3 OpenWeatherMapAPIClient.py  >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/output.log 2>&1``
	* The expression above also redirects the output from OpenWeatherMapAPIClient.py to output.log, this is mainly for debugging and is not mandatory. 
2. crontab -l 
	* View CRON jobs scheduled	

# InfluxDB Backups & Restore
Use the influx backup command to back up data and metadata stored in InfluxDB. InfluxDB copies all data and metadata to a set of files stored in a specified directory on your local filesystem.
1. cd into InfluxDB docker image shell
	* sudo docker exec -it **container_id** /bin/bash
	* e.g., ``sudo docker exec -it 85467b4a3382 /bin/bash``
2. influx backup *absolute_path_to_backup*
	* stores backup files (tar.gz) in the specified path
	* e.g., ``influx backup influxdb_backups/influxdb_backup_20230625235901``
3. influx restore *absolute_path_to_backup*
	* can be used to restore a database to a previously known state
	* e.g., ``influx restore influxdb_backups/influxdb_backup_20230625235901``

## Manually Trigger InfluxDB Backup
The **influx_db_backup.sh** bash script is used to create an InfluxDB backup. 
* You can manually trigger a backup by running the bash script ``./influx_db_backup.sh``
* InfluxDB backups exists as tar.gz files, and can be used to restore a database.
* The bash script will also copy the backup files into the InfluxDB directory. Easier way to access and view / analyze files as required. 

## Automatic Scheduling of Backups
As of writing a backup of the InfluxDB database is created daily at 2359 (SG Time). This is achieved by scheduling a CRONJOB using the expression below 
* 59 23 * * * path to influx_db_backup.sh
* e.g, ``59 23  * * * cd /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB && sudo ./influx_db_backup.sh >> /home/yappi/ITP-SE12-Power-Monitoring/InfluxDB/influxdb_backups/backup-logs.txt 2>&1``

