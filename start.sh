#! /bin/sh
python3 ftpupload.py &
python3 trapcam.py &

sleep 2m
echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness
echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness
echo 0 > /sys/class/leds/wl18xx_bt/brightness
exit 0
