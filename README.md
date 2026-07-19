# Docker Nginx Load Balancer with Flask & MySQL

## Project Overview

This project demonstrates a highly available web application architecture using Docker containers, Nginx load balancing, and MySQL database connectivity.

The solution consists of:

* MySQL Database Container
* Multiple Flask Application Containers
* Nginx Reverse Proxy & Load Balancer
* SSL/TLS Encryption
* Docker Networking

Nginx distributes incoming traffic across multiple Flask application instances, providing scalability and high availability.

## Architecture

```text
                    Internet
                        |
                        |
                  +------------+
                  |   Nginx    |
                  | LoadBalancer|
                  +------------+
                  /     |      \
                 /      |       \
                /       |        \
               v        v         v
      +------------+ +------------+ +------------+
      | Flask App1 | | Flask App2 | | Flask App3 |
      +------------+ +------------+ +------------+
               \        |         /
                \       |        /
                 \      |       /
                  v     v      v
                 +-------------+
                 |   MySQL DB  |
                 +-------------+
```

## Features

* Dockerized Flask application
* MySQL backend database
* Nginx reverse proxy
* Round-robin load balancing
* SSL/TLS encryption using self-signed certificates
* Docker bridge networking
* High availability through multiple application instances

## Technology Stack

| Component        | Technology     |
| ---------------- | -------------- |
| Application      | Flask (Python) |
| Database         | MySQL          |
| Containerization | Docker         |
| Load Balancer    | Nginx          |
| Security         | SSL/TLS        |
| Operating System | Linux          |

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── nginx
│   ├── certs
│   │   ├── nginx-selfsigned.crt
│   │   └── nginx-selfsigned.key
│   └── config
│       └── default.conf
└── README.md
```

## Create Docker Network

```bash
docker network create shopping-network
```

## Deploy MySQL Database

```bash
docker run -d \
--name shopping-database \
--network shopping-network \
-e MYSQL_ROOT_PASSWORD=mysqlroot123 \
-e MYSQL_DATABASE=shopping \
-e MYSQL_USER=shopping \
-e MYSQL_PASSWORD=shopping \
mysql:latest
```

The MySQL container stores product information and serves as the backend database.

## Build Flask Application Image

```bash
docker build -t shopping-application:v1 .
```

## Deploy Flask Application Containers

### Application Instance 1

```bash
docker run -d \
--name shopping-application-1 \
--network shopping-network \
-e DB_SERVER=shopping-database \
-e DB_USER=shopping \
-e DB_PASSWORD=shopping \
-e DB_DATABASE=shopping \
shopping-application:v1
```

### Application Instance 2

```bash
docker run -d \
--name shopping-application-2 \
--network shopping-network \
-e DB_SERVER=shopping-database \
-e DB_USER=shopping \
-e DB_PASSWORD=shopping \
-e DB_DATABASE=shopping \
shopping-application:v1
```

### Application Instance 3

```bash
docker run -d \
--name shopping-application-3 \
--network shopping-network \
-e DB_SERVER=shopping-database \
-e DB_USER=shopping \
-e DB_PASSWORD=shopping \
-e DB_DATABASE=shopping \
shopping-application:v1
```

## Generate SSL Certificates

```bash
mkdir -p nginx/{certs,config}

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout nginx/certs/nginx-selfsigned.key \
-out nginx/certs/nginx-selfsigned.crt
```

## Configure Nginx Load Balancer

Create `nginx/config/default.conf`

```nginx
upstream shopping_backends {
    server shopping-application-1:5000;
    server shopping-application-2:5000;
    server shopping-application-3:5000;
}

server {
    listen 443 ssl;

    ssl_certificate /etc/ssl/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/nginx-selfsigned.key;

    location / {
        proxy_pass http://shopping_backends;
    }
}

server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

The upstream configuration distributes requests across three Flask application containers.

## Deploy Nginx Container

```bash
docker run --name shopping-proxy \
-d \
--network shopping-network \
-v $(pwd)/nginx/certs/:/etc/ssl/ \
-v $(pwd)/nginx/config/default.conf:/etc/nginx/conf.d/default.conf \
-p 80:80 \
-p 443:443 \
nginx:alpine
```

## Access Application

HTTP:

```text
http://<server-ip>
```

HTTPS:

```text
https://<server-ip>
```

## Testing Load Balancing

Refresh the application multiple times and observe the hostname displayed on the webpage.

Requests will be distributed among:

* shopping-application-1
* shopping-application-2
* shopping-application-3

This confirms that Nginx is successfully load balancing traffic across multiple backend servers.

