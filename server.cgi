#!/bin/bash

incomingData=''
startPortRange=9000 #Ports to be released for ssh communications
endPortRange=9010
firstAvailablePort=''

# --------------------------------------------------------------------------

function readRequest() {
# To avoid internal server error (500), minimum text to echo
echo ''
# Read the number of bytes(mentioned in CONTENT_LENGTH header) and
# store the content in incomingData variable
read -n $CONTENT_LENGTH incomingData
# To view the content of the incoming data, try a test URL with POST using curl
# curl --data "requestSshCredentials" http://localhost/server
# This will send the data to server(to this cgi script) and based on availablity
# of the ports it will allocate ssh credentials
}

# --------------------------------------------------------------------------

function checkRequest() {
if [ "$incomingData" == "requestSshCredentials" ];
    then
	firstAvailablePort=$(nmap -p $startPortRange-$endPortRange localhost \
			    | grep -m 1 closed \
			    | cut -d '/' -f 1)
	# Exit if no ports available
	if [ $(echo -n $firstAvailablePort | wc -m) == "0" ];
	    then
		echo "Sorry, NO ports available, please try again!"
		exit 0
	fi
fi
}

# -------------------------------------------------------------------------

function usernamePasswdforSSH() {
	randomUser=$(date | md5sum | cut -c-5)
	randomPasswd=$(date | md5sum | cut -c6-16) #just in case :)
	encryptedPasswd=$(openssl passwd $randomPasswd)
	sudo useradd -p $encryptedPasswd -r -s /bin/false $randomUser
	echo $firstAvailablePort,$randomPasswd,$randomUser
}

# -------------------------------------------------------------------------

readRequest
checkRequest
usernamePasswdforSSH
