# ITP-SE12-Power-Monitoring
This directory contains the docker-compose.yml file used to host InfluxDB, NodeRed, Eclipse-Mosquitto and Grafana Docker Images.

## Initial Setup
This setup guide is tailored for **Google Cloud Console**. All commands were executed in the instance shell (E2-Medium, Debian-11). If you are using a different cloud provider, you will need to find alternatives to configure firewall rules. 
1. Ensure Git Repository has been cloned
	* ``git clone https://github.com/danialhbma/ITP-SE12-Power-Monitoring.git``
2. Navigate to docker-containers folder.
	* ``cd ITP-SE12-Power-Monitoring/docker-containers``
3. Install docker.io and docker-compose.
	* ``sudo apt install docker.io -y && sudo apt install docker-compose -y``
4. Start docker containers.
	* ``sudo docker-compose up -d`` 
5. Docker images are hosted on the corresponding ports: 
	* nodered: port 1880
	* influxdb: port 8086
	* grafana: port 3000
	* eclipse-mosquitto: port 1883 **not accessible via web, but acts as broker for mqtt publishers and subscribers**
6. Verify docker images are up and running.
	* ``sudo docker ps``
	* ``curl <public-ip-address>:<port>`` 
	* e.g., ``curl 35.198.233.52:8086``
7. Configure firewall rules to enable TCP access to these ports. Note that these rules will be configured for the entire project. New google cloud instances within the same project will share the same firewall rules.
	* **Depends on local machine / cloud provider used. Commands are for Google Cloud Instances only**.
	* ``gcloud compute firewall-rules create node-red-rule --allow tcp:1880``
	* ``gcloud compute firewall-rules create influxdb-rule --allow tcp:8086``
	* ``gcloud compute firewall-rules create grafana-rule --allow tcp:3000``
	* ``gcloud compute firewall-rules create allow-mqtt --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:1883 --source-ranges=0.0.0.0/0``
8. Once firewall rules configured, you should be able to access these Grafana, InfluxDB and NodeRed via an internet broweser
	* **public-ip-address:port** e.g., 35.198.233.52:8086 
	* public ip address will be the public ip address of google cloud instance / cloud provider.
9. Specific and detailed setup guides for each docker image can be found in their corresponding folders.
	* The folders contain setup guides for hosting the docker images in a Google Cloud Console Instance.

## Restarting Docker Instances
Docker images can be restarted via the following commands.
1. ``docker-compose restart``
	* Restarts all services defined in the docker-compose.yml
2. ``docker-compose restart <container_name>``
	* Restarts only the specific container 

## Docker Log Messages
To generate latest (1000) log messages for all running docker services.  
1. Navigate to error_logs directory.
	* ``cd docker_logs``
2. Run the generate_docker_logs.py script.
	* ``python3 generate_docker_logs.py``
	* log messages for will be generated in error_logs/LOG_MESSAGE directory.
	* modify the LOG_LIMIT variable here to increas log output messages.


