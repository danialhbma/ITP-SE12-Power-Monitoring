# Raspberry Pi Docker & InfluxDB Set Up
Guide on how to set up docker, InfluxDB Server and InfluxDB Client in Raspberry Pi OS.
* VM image for raspberry pi os can be found below
* https://drive.google.com/file/d/1nNXnO_8uUGSDsxkIZ_KqTpx-6qSINLRP/view?usp=share_link

## Installing Docker
1. Sudo apt install docker-io -y && sudo apt install docker-compose -y
2. sudo docker run hello-world
	* Verification step, hello-world image should be puled and executed.

## Setting Up InfluxDB Server
Steps (3) to (6) are used to configure firewall rules to allow TCP traffic to / from port 8086. Port 8086 is the port used to host the InfluxDB server. This is defined in the docker configuration file (.yml) used below.
1. cd to directory containing InfluxDB docker compose configuration file (.yml)
2. sudo docker-compose up
	* Start services defined in the .yml
	* sudo docker ps to verify that container is up and running.
	* Perform (3) to (6) if setting up InfluxDB server for the first time.
3. sudo apt-get install ufw
4. sudo ufw allow 8086/tcp
5. sudo ufw enable
6. sudo ufw status
	* Verification step to ensure firewall rules configured correctly.
	* There should be a line that shows 8086/allow in.
7. sudo docker ps
	* Verify that container is up and running and to obtain IP address of container.
8. sudo docker inspect <container ID> | grep IPAddress
	* curl IPAddress:8086 or visit IPAddress:8086 in browser e.g.,  172.18.0.2:8086
	* user: admin, password: changemeplease

## Setting UP InfluxDB Client
1. pip3 install influxdb-client
2. Retrieve toekn from InfluxDB Server
3. Replace API Token and IP Address in sample read/write codes. Run Simulator.py

