# Setting up Node-RED in Cloud
1. cd to directory containing docker-compose.yml 
	* docker compose file provided will host node red on port 1880
	* assumes that docker and docker-compose already installed
2. sudo docker-compose up -d 
	* -d flag runs node red container in the background
3. sudo docker ps 
	* verification step to confirm that node-red image successfully started
4. sudo docker inspect <container-id> | grep IPAddress
	* obtain ip address of node red 
	* run curl <ip address>:1880
	* you should see html code for node-red, if so configure firewall rules to allow tcp connections externally.
5. gcloud compute firewall-rules create node-red-rule --allow tcp:1880
	* Allows TCP connections to port 1880, you should now be able to access node-red using the public-ip address of GoogleCloud.
	* e.g., http://35.197.144.239:1880/

