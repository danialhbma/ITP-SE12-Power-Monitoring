# InfluxDB 

## Mass create buckets
1. Add bucket name and description to buckets.json
2. python3 BucketCreator.py 
	* Buckets that already exists will be ignored

## Write Data To InfluxDB Server Using Python
Writing to InfluxDB involves two classes, InfluxDBWriter and InfluxDBMeasurement (Abstract). InfluxDBMeasurement is an abstract class to be inherited, the _set_tags() and _set_fields() function must be implemented by sub-classes. 
	* Tags are used for filtering e.g., device name.
	* Fields are actual data / values e.g., Temp, Humidity etc.
	* Tags and Fields are used to create a Measurement (Point) object. 
	* InfluxDBWriter.write_single_measurement() takes in a point object, and writes this point object to InfluxDB server.
	* See OpenWeatherMapAPIClient.py and code comments for example.


## OpenWeatherMap
Makes API calls to OpenWeatherMapAPI, to retrieve weather information. Information is then written to InfluxDB server. This script will be scheduled using a CRON job and executed at 1 hourly intervals.
1. Verify API key valid.
2. Modify latitude and longitude to obtain weather information.
3. pip3 install influxdb-client
4. python3 OpenWeatherMapAPIClient.py	

## Creating CRONJOBS
1. crontab -e
	* Add this line to run a script every hour on the 10th minute 
	* 10 * * * * cd <path to folder containing script> && python3 <script name> 
2. crontab -l 
	* View CRON jobs scheduled	
