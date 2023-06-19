import datetime
import os

log_messages = []

file_path = os.path.join(".", "mqtt_logs.txt")
with open(file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    timestamp, message = line.split(": ", 1)
    timestamp = timestamp.strip()
    dt = datetime.datetime.fromtimestamp(int(timestamp))
    formatted_date = dt.strftime('%d-%m-%Y %H:%M:%S')
    log = f"{formatted_date}: {message}"
    log_messages.append(log)

with open(file_path, 'w') as file:
    file.writelines(log_messages)
