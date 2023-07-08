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
To simplify extraction of docker logs retrieval, use the **`generate_docker_logs.py`** script below. The script automatically retrieves the most recent log messages (up to 1000) for each docker image that is running. Log messages for each docker image is stored as a .txt file and will be placed in the **LOG_FILES** directory. To increase the number of log messages to retrieve, modify the **LOG_LIMIT** variable in `generate_docker_logs.py`.
1. Run `generate_docker_logs.py`
	* Retrieves the latest 1000 log messages for all docker images running
2. Check LOG_FILES directory for output 

