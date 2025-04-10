# Password Manager | Alberto Lorenzini

## Web Application
### REQUISITES:
- python >= 3.10
- pymongo == 4.12 ---> driver for mongodb used by python
- pip ---> package installer of pyhton
- Flask ---> Framework for python
- gunicorn == 22.0.0 ---> WSGI Server
- docker [[docker guide](https://docs.docker.com/engine/install/ "Guide to install Docker Engine in multiple Linux OS")]

	The installation of this packages are shown below:
	```
	sudo apt install python-3.10
	sudo apt install pip
	sudo pip install Flask pymongo==4.12 gunicorn==22.0.0
	```
---
### INSTALLATION:
The are multiple ways to install software:
1. Docker file:
	- Install docker in your system: [docker guide](https://docs.docker.com/engine/install/ "Guide to install Docker Engine in multiple Linux OS")
	- Change file /etc/hosts to reach server by name: ` vim /etc/hosts ` and add **local-ip** following with **dns-name**
	- move to directory where there's compose.yaml (EncryptPassword/passwordManager/WebSite)
	- Start docker-compose file with the command:
	```
	docker compose up -d 
	```
	- Access to your browser and search  and goes
	- Have fun

2. Source code:
	- Download the project
