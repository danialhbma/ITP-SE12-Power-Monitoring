# Setting Up Python Flask API Container
1. cd to the directory containing docker-compose file
2. ``sudo docker-compose up``
3. ``gcloud compute firewall-rules create api-rule --allow tcp:8080``
4. To test the API endpoints, visit the Grafana website > Power Analysis & Estimation Tool
    1. In Rack Power Consumption Calculation, input your desired values
    2. Click Submit
    3. Success popup should appear and results are displayed in the last 2 fields (Estimated Power Consumption and Estimated Cost)
   
   ![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/9b52bf5b-d26f-4b63-9925-aa4bcc07279c)
   ![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/adc5a649-91eb-4767-a69b-a8af677dffb4)

    1. In Container Farm Power Consumption Calculation, input your desired values
    2. Click Submit
    3. Success popup should appear and results are displaye in the Results column
    ![image](https://github.com/danialhbma/ITP-SE12-Power-Monitoring/assets/91550661/e2641d08-06a1-42c5-b899-fa6eca45c5fb)

# Reverse Proxying API Endpoints
All endpoints added in the Flask API file (calculator_app.py) need to be added into the reverse proxy setup to ensure that all requests and results are routed properly
1. cd to the directory containing nginx.conf
2. Under the server block, add the endpoint as follows:

<pre><code> location /<endpoint> {
  proxy_pass http://<ip-address>:8080/<endpoint>;
  proxy_set_header Host $http_host;
}
</code></pre>

3. Restart the nginx container by running:
`` sudo docker stop nginx ``

`` sudo docker-compose up nginx ``
