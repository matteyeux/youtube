#!/bin/bash
# script to install docker
# only debian is supported for the moment
# https://docs.docker.com/install/linux/docker-ce/debian/

echo "updating repositories"
apt update -qq

# installing dependencies
sudo apt-get -y -qq install \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg2 \
	software-properties-common


# downloading Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -

# check fingerprint
sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/debian \
	$(lsb_release -cs) \
	stable"

# updating again
apt-get update -qq

apt install -y docker-ce docker-compose docker-ce-cli containerd.io

