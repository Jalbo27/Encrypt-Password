#!/bin/bash
#preparing setup of the password manager

echo "Starting installation of Password Manager in your system..."
echo "Generating credentials for mongo..."
osrelease=$("grep -E '^(ID_LIKE)=' /etc/os-release")
rnd_user=${LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' < /dev/urandom | head -c 13; echo}
rnd_pass=${LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' < /dev/urandom | head -c 13; echo}

echo "Creation of docker.env file"
echo "# ENVIRONMENTS VARIABLES \

MONGO_INITDB_ROOT_USERNAME=\"$rnd_user\" \
MONGO_INITDB_ROOT_PASSWORD=\"$rnd_pass\" \
MONGO_INITDB_DATABASE=\"passwordManager\" \
TZ=Europe/Rome" > .docker.env 

echo "Generating license for this specific system"
openssl req -x509 -nodes -newkey rsa:2048 -keyout ./.nginx/.certs/pw-manager.key --subj 'CN=my new cert/C=SK' out ./.nginx/.certs/pw-manager.crt
cp ./.nginx/.certs/pw-manager.crt /etc/ssl/certs/

echo "Starting containsers..."
docker compose up -d --build
