#!/bin/bash

# Obtain influxDB container id
container_id=$(sudo docker ps -f "name=influxdb" -q)
echo "Container ID: $container_id"

# Create the backup directory file
backup_directory="backup_$(date +%Y%m%d)"
echo "$backup_directory"

# Enter the InfluxDB container shell create the backup directory
sudo docker exec -it "$container_id" mkdir -p "$backup_directory"

# Enter the InfluxDB container shell and run the backup command 
sudo docker exec -it "$container_id" influx backup "$backup_directory"
