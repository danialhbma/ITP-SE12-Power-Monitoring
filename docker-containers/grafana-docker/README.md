# Setting up Grafana
1. cd to directory containing docker-compose file
2. ``sudo docker-compose up``
3. ``gcloud compute firewall-rules create grafana-rule --allow tcp:3000``
4. visit publicly hosted grafana website 
	* username and password will both be admin on first login
	* following first login, a prompt will appear allowing you to change password

# Install Plugins
While the Grafana docker container is running, we can install plugins on it. This is only required for adding new plugins.

In our website, the Data Manipulation Panel by Volkov Labs (https://grafana.com/grafana/plugins/volkovlabs-form-panel/) has been installed using the following steps:

1. Get the container ID of the Grafana container using
``sudo docker ps``

2. To execute commands in the running Grafana container, use the command below and replace it with your container ID:
``sudo docker exec -it <container_id> /bin/bash``

3. Once in the Grafana container's CLI, install the Data Manipulation Plugin using:
``grafana cli plugins install volkovlabs-form-panel``

4. Restart the container
``sudo docker restart <container_id>``

# Configuration Backup
A backup of all Grafana configurations can be found in the config-backup directory. 
* [Farm Monitoring Dashboard backup](<config-backup/RP Urban Farm Monitoring JSON Model.json>)
* [Farm Rack Monitoring Dashboard backup](<config-backup/RP Urban Farm Rack Monitoring JSON Model.json>)
* [Telegram Alert Rules Backup](config-backup/templates-alert-manager-config.json)