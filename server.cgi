#!/bin/bash

incomingData=''
startPortRange=9000
endPortRange=9010

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

function checkRequest() {
if [ "$incomingData" == "requestSshCredentials" ];
	then
	firstAvailablePort=$(nmap -p $startPortRange-$endPortRange localhost \
			    | grep -m 1 closed \
			    | cut -d '/' -f 1)
	if [ $(echo -n $firstAvailablePort | wc -m) == "0" ];
		then
		echo "No ports available, please try again!"
	fi
	echo $firstAvailablePort
fi
}

readRequest
checkRequest
