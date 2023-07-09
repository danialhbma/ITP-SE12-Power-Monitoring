# Setting Up Eclipse-Mosquitto in Google Cloud
All steps performed in VM instance shell CLI.
If setting up Eclispe-Mosquitto docker image for the first time perform steps (1) to (6). Else just run (1) and (5) if docker image not up. 

1. cd to directory containing docker-compose.yml file
	* docker-compose file used will use port 1883 for eclipse-mosquitto container image.
	* Port 1883: This is the default port for MQTT communication. MQTT clients connect to the broker using this port to publish and subscribe to MQTT topics. It is a TCP-based port where MQTT messages are exchanged between clients and the MQTT broker. Port 1883 is used for native MQTT communication.

2. configure firewall rules
	* ``gcloud compute firewall-rules create allow-mqtt --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:1883 --source-ranges=0.0.0.0/0``

3. ``gcloud compute firewall-rules list``
	* Verifies firewall configured correctly, port 1883 should allow TCP connections
4. to use authentication when connecting to broker, a password file must be created. replace <path_to_passwd_file> and <username> with the actual pathname and username used:
    1. add a user to the password file: `` sudo mosquitto_passwd -c <path_to_passwd_file> <username> ``
    2. you will be prompted to enter a password for the user
    3. after reentering the password, the password file will be successfully created
6. create the mosquitto.conf file if not already created. replace <path_to_passwd_file> with the actual pathname used:
	* file should contain the following lines:
	* listener 1883
	* allow_anonymous false
 	* password_file <path_to_passwd_file>
7. ``sudo docker-compose up``
	* starts eclipse-mosquitto docker container
8. To verify that MQTT broker is correctly configured, open two new terminals, one will serve as a publisher and the other will serve as subscriber. 
	* ``mosquitto_sub -h <ip address of cloud instance> -p 1883 -t <topic_name> -u <username> -P <password>``
	* ``mosquitto_pub -h <ip_address of cloud instance> -p 1883 -t <topic_name> -u <username> -P <password> -m "Hello, MQTT!"``
	* You should see "Hello, MQTT!" in the CLI that is the subcriber

