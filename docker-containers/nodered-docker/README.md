# Setting up Node-RED in Cloud
All steps performed in Google Cloud VM shell / CLI.

1. cd to directory containing docker-compose.yml 
	* docker compose file provided will host node red on port 1880
	* assumes that docker and docker-compose already installed
	* ``cd nodered-docker``
2. ``sudo docker-compose up -d`` 
	* -d flag runs node red container in the background
3. ``sudo docker ps`` 
	* verification step to confirm that node-red image successfully started
4. ``sudo docker inspect <container-id> | grep IPAddress``
	* obtain ip address of node red 
	* ``run curl <ip address>:1880``
	* you should see html code for node-red, if so configure firewall rules to allow tcp connections externally.
5. ``gcloud compute firewall-rules create node-red-rule --allow tcp:1880``
	* Adds a new firewall rule that allows TCP connections to port 1880, you should now be able to access node-red using the public-ip address of GoogleCloud.

# Securing node-red
To restrict access from your publicly hosted node-red image, you can set login credentials.
1. Ensure that node-red image is running, and that you can access the node-red server via the web browser.
2. ``sudo docker ps``
	* copy the container-id for the node-red container
3. ``docker exec -it <container-id> /bin/bash``
	* access node red container shell
4. ``node-red admin hash-pw``
	* node-red requires passwords to be securely hashed using the bcrypt algorithm.
	* after running this command, a prompt to enter a password will appear in the node-red container shell.
	* enter in your desired password and copy the hashed version of it.
5. cd to settings.js 
	* **uncomment out the adminAuth: {} section**
	* replace password with your desired password
	* see https://nodered.org/docs/user-guide/runtime/securing-node-red for more information
