# Setting up NGINX
1. cd to directory containing docker-compose file

2. ``sudo docker-compose up``

3. Ensure that the Grafana docker container is running:
``sudo docker ps``

4. To verify that the reverse proxy has been set up, navigate to https://<public-ip-address> (e.g. https://35.198.233.52). You should see the Grafana login page.

# Generating Self-Signed SSL Certificates
To use HTTPS, SSL certificates are needed. This section takes you through how to generate your own self-signed SSL certificates which will be used by NGINX

1. Create a new directory to store your key and certificate:
``sudo mkdir ssl-certs``

2. Navigate to the new directory
``cd ssl-certs``

3. Use openssl to generate the key:
``sudo openssl genrsa -out private.key 2048``

4. To generate a signed certificate, you need a certificate signing request (CSR). Run the following command to create one:
``sudo openssl req -new -key private.key -out private.csr``

5. You can use your new CSR to obtain a valid certificate from a certificate authority (CA). Alternatively, you can generate a self-signed certificate that's valid for 1 year by running the following:
``sudo openssl x509 -req -days 365 -in private.csr -signkey private.key -out private.crt``
