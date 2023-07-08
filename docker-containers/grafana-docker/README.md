# Setting up Grafana
1. cd to directory containing docker-compose file
2. ``sudo docker-compose up``
3. ``gcloud compute firewall-rules create grafana-rule --allow tcp:3000``
4. visit publicly hosted grafana website 
	* username and password will both be admin on first login
	* following first login, a prompt will appear allowing you to change password

# Configuration Backup
A backup of all Grafana configurations can be found in the config-backup directory. 
* [Farm Monitoring Dashboard backup](<config-backup/RP Urban Farm Monitoring JSON Model.json>)
* [Farm Rack Monitoring Dashboard backup](<config-backup/RP Urban Farm Rack Monitoring JSON Model.json>)
* [Telegram Alert Rules Backup](config-backup/templates-alert-manager-config.json)