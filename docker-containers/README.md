# ITP-SE12-Power-Monitoring
This directory contains the docker-compose.yml file used to host InfluxDB, NodeRed, Eclipse-Mosquitto and Grafana Docker Images.

## Usage
To run these images locally or in a seperate device. 
1) Clone the repository to your local machine.
	* git clone https://github.com/danialhbma/ITP-SE12-Power-Monitoring.git 
2) Navigate to docker-containers folder.
3) Run the following commands, the first command starts up the docker images, while the second command displays the list of running docker images.
	* sudo docker-compose up -d 
	* sudo docker ps 
4) Specifc and detailed setup guides for each docker image can be found in their corresponding folders.
	* The folders contain setup guides for hosting the docker images in a Google Cloud Console Instance.


## Docker Log Messages
To easily view log messages
1) Navigate to error_logs directory
2) Run the generate_docker_logs.py script
	* log messages for will be generated in error_logs/LOG_MESSAGE directory

