#!/bin/bash
#preparing setup of the password manager

stty -echoctl
PATH_PRODUCT_CERTS=".nginx/.certs"
PATH_SYSTEM_CERTS="/etc/ssl/certs"
certificate=1

trap ctrl_c INT

function ctrl_c(){
	echo -e "\n\nExited"
	exit;
}



# CHECK FOR THE ALL REQUIRED PACKAGES INSTALLED
function checkRequisites 
{
	check=0
	### CHECK FOR DOCKER COMMAND
	if [ ! docker 2>&1 > /dev/null ]; then
		printf "\ndocker is not installed..."
	else
		printf "\ndocker is installed, check for openssl... \u2714\ufe0f"
		check=1
	fi
	### CHECK FOR OPENSSL COMMAND
	if [ ! openssl 2>&1 > /dev/null ]; then
		printf "\nopenssl is not installed..."
		check=0
	else
		printf "\nopenssl is installed, check for file... \u2714\ufe0f"
		check=1
	fi
	### CHECK FOR FILE COMMAND
	if [ ! file 2>&1 > /dev/null ]; then
		printf "\nfile is not installed..."
		check=0
	else
		printf "\nfile is installed... \u2714\ufe0f"
		check=1
	fi

	if [ $check==1 ]; then
		printf "\n\nAll requisites are installed \u2714\ufe0f"
	else
		printf "\n\nSome requisites are not installed"
		printf "Install necessary packages based by your system"
	fi
}


function usage
{
	echo -e "\nPASSWORD MANAGER INSTALLER SETUP: "
	echo "Usage: ./install.sh OPTIONS [FILE]"
	echo "Help: ./install.sh -h|--help"
	echo ""
	echo -e "Options:
	-h, 	--help			Get Help informations about the script.
	-i,	--install		First installation of the product, also install a custom certificate for this specific machine.
		--new-certificate	Install new certificate for the product only in this machine!.
	-c, 	--certificate		Specific certificate file [*.pkcs, *.crt, *.pem].
	-k, 	--certificate-key	Specify the key of the certificate passed by the other parameter (required --new-certificate parameter).
	--no-certificate		Specify that the program runs only in https without certificate (requires -i|--install option).
	
EXAMPLES:
	./install.sh OR ./install.sh -i|--install			--> First installation with a valid auto generated certificate.
	./install.sh --new-certificate					--> Generate and install a new certificate.
	./install.sh -c|--certifcate [FILE] -k|--certificate-key [FILE]	--> Specify a custom certificate and a valid key of the certification."
}


function firstInstall
{
	if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then	
		echo "stopping existing services of the product..."
		docker stop $(docker ps -aqf "name=website-mongo-1")
		docker stop $(docker ps -aqf "name=website-nginx-1")
		docker stop $(docker ps -aqf "name=website-password-manager-1")
		echo -e "\nThere are just existing services up\nExiting...\n"
		exit;
	fi
	
	echo -e "\nStarting the first installation of Password Manager in your system..."
	echo -e "\nPreparing directories..."
	if [ ! -d .nginx/ -a ! -d .nginx/.certs/ ]; then
		echo -e "Directories creation done"
		mkdir .nginx/ .nginx/.certs/ 
		cp default.conf .nginx/
		cp default_https.conf .nginx/
	fi
	if [ $certificate == 0 ]; then
		sed -e '/CMD/c\CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]' -i Dockerfile
		sed -e 's|      - ./.nginx/default.conf:/etc/nginx/conf.d/default.conf|      - ./.nginx/default_https.conf:/etc/nginx/conf.d/default.conf|' -i compose.yaml
		sed '/secrets\|(file)\|key\|cert/s/^/#/g' -i compose.yaml
		sed '/443/c\- "80:80"' -i compose.yaml
		sed '/http-equiv/s/^/<!--/g' -i templates/homepage.html templates/register.html
		sed '/http-equiv/s/$/-->/g' -i templates/homepage.html templates/register.html
	else
		sed -e '/CMD/c\CMD ["gunicorn", "--certfile=/run/secrets/cert", "--keyfile=/run/secrets/key", "-b", "0.0.0.0:8000", "app:app"]' -i Dockerfile
		sed -e 's|      - ./.nginx/default_https.conf:/etc/nginx/conf.d/default.conf|      - ./.nginx/default.conf:/etc/nginx/conf.d/default.conf|' -i compose.yaml
		sed '/secrets\|(file)\|key\|cert/s/^#*//g' -i compose.yaml
		sed '/80/c\- "443:443"' -i compose.yaml
		sed '/http-equiv/s/^/^<!--*//g' -i templates/homepage.html
	fi
	
	echo -e "Generating credentials for mongo...\r"
	osrelease=$(grep -E '^(ID_LIKE)=' /etc/os-release)
	rnd_pass=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	rnd_user=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	#rnd=$(LC_ALL=C tr -dc 'A-Za-z0-9!#%&''()*\'',-./:;<=>?[\]^_`{|}~' < /dev/urandom | head -c 13; echo)
	echo "Creation of docker.env file"
	echo -e "# ENVIRONMENTS VARIABLES\n\nMONGO_INITDB_ROOT_USERNAME=\""$rnd_user"\"\nMONGO_INITDB_ROOT_PASSWORD=\""$rnd_pass"\"\nMONGO_INITDB_DATABASE=\"passwordManager\"\nTZ=Europe/Rome" > .docker.env 

	if [ $certificate == 1 ]; then
		newCertificate
	else
		echo -e "\nStarting services..."
		docker compose up -d --build > /dev/null 2>&1
	fi
}


function newCertificate
{
    	if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then
		echo "stopping existing services of the product..."
		docker stop $(docker ps -aqf "name=website-mongo-1")
		docker stop $(docker ps -aqf "name=website-nginx-1")
		docker stop $(docker ps -aqf "name=website-password-manager-1")
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
		cp $PATH_PRODUCT_CERTS/pw-managerRootCA.crt /etc/ssl/certificates
	else
		cp $PATH_PRODUCT_CERTS/pw-managerRootCA.crt /etc/ssl/certificates
	fi
	
	# IF EXIST RESTART CONTAINERS
	echo -e "\nStarting services..."
	if [ docker inspect webiste-mongo-1 > /dev/null 2>&1 -a docker inspect website-password-manager-1 > /dev/null 2>&1 -a docker inspect website-nginx-1 > /dev/null 2>&1 ]; then
		docker start $(docker ps -aqf "name=website-mongo-1")
		docker start $(docker ps -aqf "name=website-nginx-1")
		docker start $(docker ps -aqf "name=website-password-manager-1")
    else
		docker compose up -d --build > /dev/null 2>&1
    fi
}


# INSTALL A SPECIFIC CERTIFICATE PASSED BY FILE FROM USER
function installCertificate
{
	if [ -e $2 ]; then
		if [ $(file $2 | grep -o "PEM certificate") != "" ]; then	
			if [ -d /usr/share/applications/ca-certificates/mozilla ]; then
				cp $2 /usr/share/ca-certificates/mozilla/
				cp $2 .nginx/.certs/pw-managerRootCA.crt
				ln -s /usr/share/ca-certificates/mozilla/pw-managerRootCA.crt /etc/ssl/certs/pw-managerRootCA.pem
			else
				cp $2 /etc/ssl/certificates/
			fi
		fi
	else
		echo -e "\nYou have to specify a file [*.pem, *.crt, *.pkcs] or a path to the file"
		echo -e "\nExample:\n"
		echo -e "\n./install --first --certificate file.crt|pem|pkcs"
		echo -e	"\n./install --first --certificate /path/to/certificate.crt|pem|pkcs"	
	fi
}

function installCertificateKey
{
	if [ -e $2 ]; then
		if [ $(file $2 | grep -o "key") != "" ]; then
			rm .nginx/.certs/*.key > /dev/null 2>&1	
			cp $2 .nginx/.certs/rootCA.key
		fi
	else
		echo -e "\nYou have to specify a key bind with the cert or a path to the file -- [*.key]"
		echo -e "\nExample:\n"
		echo -e "\n./install --first -c|--certificate <filename>.crt|pem|pkcs -k|--certificate-key <filename>.key"
		echo -e	"\n./install --first -c|--certificate /path/to/certificate.crt|pem|pkcs -k|--certificate-key /path/to/key.key"
		echo -e "\n./install --first -k|--certificate-key"
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
		-i|--install)
			if [ ! -z $2 ]; then
				if [ $2 == "--no-certificate" ]; then
					certificate=0
				else
					certificate=1
				fi
			fi
			checkRequisites
			firstInstall
			exit 1
	    ;;
		--no-certificate)
			echo "Requires to be with --install option."
			exit 1
		;;
		-c|--certificate)
			checkRequisites
			installCertificate
			shift
	    ;;
		-k|--certificate-key)
			checkRequisites
			installCertificateKey
			shift
		;;
	esac
done
