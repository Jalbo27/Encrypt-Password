#!/bin/bash
#preparing setup of the password manager


PATH_PRODUCT_CERTS="./.nginx/.certs"
PATH_SYSTEM_CERTS="/etc/ssl/certs"

function checkRequisites 
{
	check=0
	### CHECK FOR DOCKER
	if [ ! docker 2>&1 > /dev/null ]; then
		printf "\ndocker is not installed..."
	else
		printf "\ndocker is installed, check for openssl..."
		check=1
	fi
	### CHECK FOR OPENSSL
	if [ ! openssl 2>&1 > /dev/null ]; then
		printf "\nopenssl is not installed..."
		check=0
	else
		printf "\nopenssl is installed..."
		check=1
	fi

	if [ $check==1 ]; then
		printf "\n\nAll requisites are installed"
	else
		printf "\n\nSome requisites are not installed"
		printf "Install necessary packages based by your system"
	fi
}


function usage
{
	echo -e "\nPASSWORD MANAGER INSTALLER SETUP: "
	echo "Usage: ./install.sh [OPTIONS] "
	echo "Help: ./install.sh [-h|--help]"
	echo ""
	echo -e "Options:\n \
	-h, --help		Get Help informations about the script\n \
	-md, --read-me		Read the README.md file\n \
	--first			First installation of the product\n \
	--new-certificate	Install new certificate for the product only in this machine!"
}


function firstInstall
{
	if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then	
		echo "stopping existing services of the product..."
		docker stop $(docker ps -aqf "name=website-mongo-1")
		docker stop $(docker ps -aqf "name=website-nginx-1")
		docker stop $(docker ps -aqf "name=website-password-manager-1")
	fi
	
	echo -e "\nStarting the first installation of Password Manager in your system..."
	echo -e "\nPreparing directories..."
	mkdir .nginx .nginx/.certs 
	mv default.conf ./.nginx
	echo "Generating credentials for mongo..."
	sleep 2
	osrelease=$(grep -E '^(ID_LIKE)=' /etc/os-release)
	rnd_pass=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	rnd_user=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	rnd=$(LC_ALL=C tr -dc 'A-Za-z0-9!#%&''()*\'',-./:;<=>?[\]^_`{|}~' < /dev/urandom | head -c 13; echo)

	echo "Creation of docker.env file"
	echo -e "# ENVIRONMENTS VARIABLES\n\nMONGO_INITDB_ROOT_USERNAME=\""$rnd_user"\"\nMONGO_INITDB_ROOT_PASSWORD=\""$rnd_pass"\"\nMONGO_INITDB_DATABASE=\"passwordManager\"\nTZ=Europe/Rome" > .docker.env 

	sleep 3
	newCertificate
}


function README
{
	cat Readme.md
}


function newCertificate
{
        if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then
                echo "stopping existing services of the product..."
                docker stop $(docker ps -aqf "name=website-mongo-1")
                docker stop $(docker ps -aqf "name=website-mongo-1")
                docker stop $(docker ps -aqf "name=website-mongo-1")
        fi

	if [ -e $PATH_SYSTEM_CERTS/pw-managerRootCA.pem ]; then
		rm $PATH_SYSTEM_CERTS/pw-managerRootCA.pem
	fi
	if [ -e /usr/share/ca-certificates/mozilla/pw-managerRootCA.crt ]; then
		rm /usr/share/ca-certificates/mozilla/pw-managerRootCA.crt
	fi

	# GENERATE CERTIFICATE
	echo -e "\nGenerating the new license for this specific system"
	openssl req -x509 -newkey rsa:4096 -keyout $PATH_PRODUCT_CERTS/rootCA.key -out $PATH_PRODUCT_CERTS/pw-managerRootCA.crt -sha256 -days 365 -nodes \
	-subj "/CN=jalbopass.com/C=ST/ST=Some-State/L=Some-City/O=Jalbo Industries S.p.A/OU=Jalbo PW-Manager Root CA" > /dev/null 2>&1 

	if [ -d /usr/share/applications/ca-certificates/mozilla ]; then
		cp $PATH_PRODUCT_CERTS/pw-managerRootCA.crt /usr/share/ca-certificates/mozilla/
		ln -s /usr/share/ca-certificates/mozilla/pw-managerRootCA.crt /etc/ssl/certs/pw-managerRootCA.pem
	else
		cp $PATH_PRODUCT_CERTS/pw-managerRootCA.crt /etc/ssl/certificates
	fi
	
	# IF EXIST RESTART CONTAINERS
	echo -e "\nStarting services..."
	sleep 5	
	if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then
                docker start $(docker ps -aqf "name=website-mongo-1")
		docker start $(docker ps -aqf "name=website-nginx-1")
                docker start $(docker ps -aqf "name=website-password-manager-1")
        else
                docker compose up -d --build > /dev/null 2>&1
        fi
}

# MANAGE OPTIONS
while [[ $# -gt 0  ]]; do
	key="$1"

	case $key in
		-h|--help)
			usage
			shift
	     ;;
		--new-certificate)
			checkRequisites
			newCertificate
			shift
	     ;;
     		--md|--read-me)
			README
			shift
	     ;;
     		--first)
			checkRequisites
			firstInstall
			shift
	     ;;
	esac
done
