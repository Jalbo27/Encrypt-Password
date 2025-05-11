# Password Manager | Alberto Lorenzini

## Web Application
### PACKAGES USED:
- python >= 3.10
- pymongo == 4.12 ---> driver for mongodb for python
- pip ---> package installer of pyhton
- Flask ---> Framework for python
- gunicorn == 22.0.0 ---> WSGI Server
- cryptography == 39.0.1 ---> library for symmetric encryption
- flask_jwt_extended ---> library for jwt codes management and csrf prevention
- openssl ---> tool for generating certificates
- docker [[docker guide](https://docs.docker.com/engine/install/ "Guide to install Docker Engine in multiple Linux OS")]

	The installation of this packages are shown below:
	```
	sudo apt install python-3.10 openssl pip
 	```
  	```
	sudo pip install Flask flask_jwt_extended pymongo==4.12 gunicorn==22.0.0 cryptography==39.0.1
	```
---
### INSTALLATION:
The are multiple ways to install software:
1. Docker file:
	- Install docker in your system: [docker guide](https://docs.docker.com/engine/install/ "Guide to install Docker Engine in multiple Linux OS")
	- Change file /etc/hosts to reach server by name: ` vim /etc/hosts ` and add **local-ip** following with **dns-name**
	- Move to directory where there's compose.yaml (default path: Encrypt-Password/passwordManager/WebSite)
	- Start docker-compose file with the command:
	```
	docker compose up -d 
	```
	- Access to your browser and search  and goes
	- Have fun

2. Installation script:
	- Download the project
	- Inside the WebSite folder there is a script named ` install.sh `
	- Execute the script via **` sudo `** or from **root** user
	- Execute ` docker ps ` to ensure that all services are up and are to be shown in this way:
	![](install.png)
	- The website has [https://jalbopass.com](https://jalbopass.com) as default dns name and all requests are forwaded to this name
	- Change file /etc/hosts to reach server by your prefered name: ` vim /etc/hosts ` and add **local-ip** following with **dns-name** below IPv4 settings
 	- Then have fun
