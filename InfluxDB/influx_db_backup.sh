#!/bin/bash

# Obtain influxDB container id
container_id=$(sudo docker ps -f "name=influxdb" -q)
echo "Container ID: $container_id"

# Create the backup directory file
backup_directory="influxdb_backup_$(date +%Y%m%d%H%M%S)"
echo "$backup_directory"

# Enter the InfluxDB container shell create the backup directory
sudo docker exec -t "$container_id" mkdir -p "$backup_directory"

# Validation check to ensure backup_directory successfully created
mkdir_exit_code=$?
if [ $mkdir_exit_code -eq 0 ]; then
  echo "Backup directory created successfully."
else
  echo "Failed to create backup directory."
  exit 1
fi

# Enter the InfluxDB container shell and run the backup command 
sudo docker exec -t "$container_id" influx backup "$backup_directory"

# Validation check to ensure backups created successfully
backup_exit_code=$?

if [ $backup_exit_code -eq 0 ]; then
  echo "Backup created successfully."
else
  echo "Failed to create backup."
  exit 1
fi

# Copy the files from docker image and into local machine
sudo docker cp $container_id:$backup_directory .
