import datetime
import os

log_messsage = []

file_path = os.path.join(".","mqtt_logs.txt")
with open(file_path, 'r') as file:
	lines = file.readlines()

for line in lines:
	timestamp, message = line.split(": ", 1)
	dt = datetime.datetime.fromtimestamp(int(timestamp))
	formatted_date = dt.strftime('%d-%m-%Y %H:%M:%S')
	print(f"{formatted_date}: {message}")
    
