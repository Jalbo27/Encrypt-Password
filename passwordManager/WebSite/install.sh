#!/bin/bash
#preparing setup of the password manager

stty -echoctl
PATH_PRODUCT_CERTS=".nginx/.certs"
PATH_SYSTEM_CERTS="/etc/ssl/certs"
certificate=1
verbose=0

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
	if ! command -v docker 2>&1 > /dev/null; then
		printf "\ndocker is not installed..."
	else
		printf "\ndocker is installed, check for openssl... \u2714\ufe0f"
		check=1
	fi
	### CHECK FOR OPENSSL COM4MAND
	if ! command -v openssl 2>&1 > /dev/null; then
		printf "\nopenssl is not installed..."
		check=$(expr $check - 1)
		check=$(echo ${check#-})
	else
		printf "\nopenssl is installed, check for file... \u2714\ufe0f"
		check=$(expr $check + 1)
		check=$(echo ${check#-})
	fi
	### CHECK FOR FILE COMMAND
	if ! command -v file 2>&1 > /dev/null; then
		printf "\nfile is not installed..."
		check=$(expr $check - 1)
		check=$(echo ${check#-})
	else
		printf "\nfile is installed... \u2714\ufe0f"
		check=$(expr $check + 1)
		check=$(echo ${check#-})
	fi

	if [ $check -eq 3 ]; then
		printf "\n\nAll requisites are installed \u2714\ufe0f"
	elif [ $check -eq 0 ]; then
		printf "None of the requisites are installed... exiting"
		exit 0;
	elif [ $check > 0 ] && [ $check < 3 ]; then
		printf "\n\n$check requisites are not installed"
		printf "Install necessary packages based by your system first, then retry the install"
		exit 0;
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
	-c, 	--cert			Specific certificate file [*.pkcs, *.crt, *.pem].
	-k, 	--cert-key		Specify the key of the certificate passed by the other parameter (required --new-certificate parameter).
	--tz,	--time-zone="TZ"	Specify the time zone
	
EXAMPLES:
	./install.sh OR ./install.sh -i|--install			--> First installation with a valid auto generated certificate.
	./install.sh --new-certificate					--> Generate and install a new certificate.
	./install.sh -c|--certifcate [FILE] -k|--certificate-key [FILE]	--> Specify a custom certificate and a valid key of the certification.
	./install.sh --tz=\"TZ\"|--time-zone=\"TZ\"			--> Specify the time zone of the product (It's for logs' purposes)"
}


function firstInstall ()
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
		if [ $verbose -eq 1 ]; then
			mkdir -v .nginx/ .nginx/.certs/ 
			mv -v default.conf .nginx/
		else
			mkdir .nginx/ .nginx/.certs/ 
			mv default.conf .nginx/
		fi
	fi
	
	echo -e "Generating credentials for mongo...\r"
	osrelease=$(grep -E '^(ID_LIKE)=' /etc/os-release)
	rnd_pass=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	rnd_user=$(LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 13; echo)
	#rnd=$(LC_ALL=C tr -dc 'A-Za-z0-9!#%&''()*\'',-./:;<=>?[\]^_`{|}~' < /dev/urandom | head -c 13; echo)
	echo "Creation of docker.env file"
	if [[ $# -gt 0 ]]; then
		echo -e "# ENVIRONMENTS VARIABLES\n\nMONGO_INITDB_ROOT_USERNAME=\""$rnd_user"\"\nMONGO_INITDB_ROOT_PASSWORD=\""$rnd_pass"\"\nMONGO_INITDB_DATABASE=\"passwordManager\"\nTZ=\"$1\"" > .docker.env 
		sed '/TZ/c\      - TZ='$1'' -i compose.yaml
	else
		echo -e "# ENVIRONMENTS VARIABLES\n\nMONGO_INITDB_ROOT_USERNAME=\""$rnd_user"\"\nMONGO_INITDB_ROOT_PASSWORD=\""$rnd_pass"\"\nMONGO_INITDB_DATABASE=\"passwordManager\"\nTZ="$(cat /etc/timezone) > .docker.env 
		sed '/TZ/c\      - TZ='$(cat /etc/timezone)'' -i compose.yaml
	fi

	time=$(date +%s 2>&1)
	newCertificate
	echo -e "\nStarting services..."
	post_start_time=$(date +%s 2>&1)

	echo -e "\nTime for starting services: "$(expr $post_start_time - $time)" seconds\n"
	echo -e "\n\nProgram is installed now! Great! You can play with it at https://jalbopass.com"
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
	if [ $verbose -eq 1 ]; then
		openssl req -x509 -newkey rsa:4096 -keyout $PATH_PRODUCT_CERTS/rootCA.key -out $PATH_PRODUCT_CERTS/pw-managerRootCA.crt -sha256 -days 365 -nodes \
		-subj "/CN=jalbopass.com/C=ST/ST=Some-State/L=Some-City/O=Jalbo Industries S.p.A/OU=Jalbo PW-Manager Root CA"
	else
		openssl req -x509 -newkey rsa:4096 -keyout $PATH_PRODUCT_CERTS/rootCA.key -out $PATH_PRODUCT_CERTS/pw-managerRootCA.crt -sha256 -days 365 -nodes \
		-subj "/CN=jalbopass.com/C=ST/ST=Some-State/L=Some-City/O=Jalbo Industries S.p.A/OU=Jalbo PW-Manager Root CA" > /dev/null 2>&1 
	fi

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
		if [ $verbose -eq 1 ]; then
			docker compose up -d --build
		else
			docker compose up -d --build > /dev/null 2>&1
		fi
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
		echo -e	"\n./install --install --cert /path/to/certificate.crt|pem|pkcs"	
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
		echo -e "\n./install --first -c|--cert <filename>.crt|pem|pkcs -k|--certificate-key <filename>.key"
		echo -e	"\n./install --first -c|--cert /path/to/certificate.crt|pem|pkcs -k|--certificate-key /path/to/key.key"
		echo -e "\n./install --first -k|--cert-key"
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
			checkRequisites
			if [ $2=='--tzt' -o $2=='--time-zone' ]; then
				firstInstall $3
			else
				firstInstall
			fi
			exit 1
		;;
		-v|--verbose)
			verbose=1
			shift
		;;
		-c|--cert)
			checkRequisites
			installCertificate
			shift
	    	;;
		-k|--cert-key)
			checkRequisites
			installCertificateKey
			shift
	    	;;
	esac
done
