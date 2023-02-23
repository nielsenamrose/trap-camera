#!/bin/sh
destination=192.168.1.10:/media/usb/trapcam
username=debian
password=temppwd

while true; do
	for filename in *[!part]?.avi*; do
		if [ -f $filename ]; then
			sshpass -p $password scp -q $filename $user@$destination && rm -f $filename
		fi
	done
	sleep 1m
done
