# Setting Up Eclipse-Mosquitto in Google Cloud
All steps performed in VM instance shell CLI.
If setting up Eclispe-Mosquitto docker image for the first time perform steps (1) to (6). Else just run (1) and (5) if docker image not up. 

1. cd to directory containing docker-compose.yml file
	* docker-compose file used will use two ports, 1883 and 9001 for eclipse-mosquitto container image.
	* Port 1883: This is the default port for MQTT communication. MQTT clients connect to the broker using this port to publish and subscribe to MQTT topics. It is a TCP-based port where MQTT messages are exchanged between clients and the MQTT broker. Port 1883 is used for native MQTT communication.
	* Port 9001: This is the default port for MQTT over WebSocket. MQTT over WebSocket allows MQTT clients to establish a connection to the MQTT broker using a standard WebSocket connection. It enables MQTT communication over the web using a browser or WebSocket-capable client applications. Port 9001 is used for MQTT communication encapsulated within the WebSocket protocol.
2. configure firewall rules
	* ``gcloud compute firewall-rules create allow-mqtt --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:1883 --source-ranges=0.0.0.0/0``
	* ``gcloud compute firewall-rules create allow-mqtt-websocket --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:9001 --source-ranges=0.0.0.0/0``
3. ``gcloud compute firewall-rules list``
	* Verifies firewall configured correctly, ports 1883 and 9001 should allow TCP connections
4. create the mosquitto.conf file if not already created.
	* file should contain the following lines:
	* listener 1883
	* listener 9001
	* allow_anonymous false
5. ``sudo docker-compose up``
	* starts eclipse-mosquitto docker container
6. To verify that MQTT broker is correctly configured, open two new terminals, one will serve as a publisher and the other will serve as subscriber. 
	* ``mosquitto_sub -h <ip address of cloud instance> -p 1883 -t <topic_name>``
	* ``mosquitto_pub -h <ip_address of cloud instance> -p 1883 -t <topic_name> -m "Hello, MQTT!"``
	* You should see "Hello, MQTT!" in the CLI that is the subcriber

