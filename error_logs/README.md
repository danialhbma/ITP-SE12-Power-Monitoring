# Retrieve Error Logs
1. sudo docker ps
	* Obtain containter ID
2. sudo docker log <container id> > <output_filename.txt>
	* Redirects output from log to an output file 
	* For docker containers that don't out to stdout i.e., output to stderr instead (eclipse-mqtt) use
		* e.g., sudo docker logs aaaf5cdb5264 > mqtt_logs.txt 2>&1 instead 
3. cat output.txt
