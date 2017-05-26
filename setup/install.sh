#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo " [!]This script must be run as root" 1>&2
   exit 1
fi

IFS='/' read -a array <<< pwd

if [[ "$(pwd)" != *setup ]]
then
    cd ./setup
fi

version=$( lsb_release -r | grep -oP "[0-9]+" | head -1 )
if lsb_release -d | grep -q "Fedora"; then
	Release=Fedora
	dnf install -y python-devel m2crypto python-m2ext swig python-iptools python3-iptools
	pip install zlib_wrapper
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install macholib
	pip install flask
	pip install pyinstaller
    pip install maproxy
elif lsb_release -d | grep -q "Kali"; then
	Release=Kali
	apt-get install python-dev
	apt-get install python-m2crypto
	apt-get install swig
	apt-get install python-pip
	pip install zlib_wrapper
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install macholib
	pip install flask
	pip install pyinstaller
    pip install maproxy
elif lsb_release -d | grep -q "Ubuntu"; then
	Release=Ubuntu
	apt-get install python-pip python-dev build-essential 
	pip install --upgrade pip 
	apt-get install python-m2crypto
	apt-get install swig
	pip install zlib_wrapper
	pip install pycrypto
	pip install iptools
	pip install pydispatcher
	pip install macholib
	pip install flask
    pip install pyinstaller
    pip install maproxy
else
	echo "Unknown distro - Debian/Ubuntu Fallback"
    apt-get install python-pip python-dev build-essential 
    pip install --upgrade pip 
    apt-get install python-m2crypto
    apt-get install swig
    pip install zlib_wrapper
    pip install pycrypto
    pip install iptools
    pip install pydispatcher
    pip install macholib
    pip install flask
    pip install maproxy
fi

# set up the database schema
./setup_database.py

# generate a cert
./cert.sh

# Support non-root instalation of DB
chown $(logname):$(logname) ../data/empyre.db

cd ..

echo -e '\n [*] Setup complete!\n'
