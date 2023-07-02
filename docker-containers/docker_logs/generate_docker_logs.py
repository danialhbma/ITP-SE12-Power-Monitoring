#!/usr/bin/env python3
import subprocess
import os
import datetime
import pytz

DESTINATION_FOLDER = "LOG_FILES"
LOG_LIMIT = "1000" # Modify this to increase length of log messages

def get_container_info():
    # Run 'docker ps' command to obtain container information
    process = subprocess.Popen(['sudo', 'docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode('utf-8')}")
        return []

    # Extract container ID, and container name from the output
    lines = output.decode('utf-8').split('\n')
    container_info = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) > 1:
            container_id = parts[0]
            container_name = parts[-1]
            container_info.append((container_id, container_name))

    return container_info

def run_docker_logs(container_id, container_name):
    # Run 'docker logs' command and redirect output to a log file
    file_name = f"{container_name}_logs.txt"
    output_file = os.path.join(".",DESTINATION_FOLDER,file_name)
    with open(output_file, 'w') as f:
        process = subprocess.Popen(['sudo', 'docker', 'logs', '--tail', LOG_LIMIT, container_id], stdout=f, stderr=subprocess.STDOUT)
        _, error = process.communicate()
        if error:
            print(f"An error occurred: {error.decode('utf-8')}")

def parse_mqtt_logs(container_name):
    log_messages = []
    file_name = f"{container_name}_logs.txt"
    file_path = os.path.join(".", DESTINATION_FOLDER, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
   
    for line in lines:
        timestamp, message = line.split(": ", 1)
        timestamp = timestamp.strip()
        dt = datetime.datetime.fromtimestamp(int(timestamp))
        dt_utc = pytz.utc.localize(dt)
        dt_local = dt_utc.astimezone(pytz.timezone('Asia/Singapore'))
        formatted_date = dt_local.strftime('%d-%m-%Y %H:%M:%S')
        log = f"{formatted_date}: {message}"
        log_messages.append(log)

    with open(file_path, 'w') as file:
        file.writelines(log_messages)

# Get container information
containers = get_container_info()

# Ensures destination folder exists
if not os.path.exists(DESTINATION_FOLDER):
	os.mkdir(DESTINATION_FOLDER)

# Run 'docker logs' command for each container
for container_id, container_name in containers:
    run_docker_logs(container_id, container_name)
    if "mosquitto" in container_name:
      	parse_mqtt_logs(container_name)
    print(f"Generated Logs for {container_name}")

