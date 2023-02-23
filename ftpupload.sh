#!/bin/sh
url=ftp://192.168.1.1/trapcam/
username=user
password=user

while true; do
	for filename in *[!part]?.avi*; do
		if [ -f $filename ]; then
			curl -u $username:$password -T $filename $url && rm -f $filename
		fi
	done
	sleep 1m
done
