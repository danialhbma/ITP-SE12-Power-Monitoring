# Manually Retrieve Docker Logs
Execute these commands in instance shell.
1. sudo docker ps
	* Obtain containter ID
2. sudo docker log <container id> > <output_filename.txt>
	* Redirects output from log to an output file 
	* For docker containers that don't out to stdout i.e., output to stderr instead (eclipse-mqtt) use
		* e.g., sudo docker logs aaaf5cdb5264 > mqtt_logs.txt 2>&1 instead 
3. cat output.txt

# Automatically Retrieve Docker Logs
1. Run generate_docker_logs.py
	* Retrieves the latest 1000 log messages for all docker images running
2. Check LOG_FILES  directory for output 

