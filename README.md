# Learning project 2: Trap camera

## The development environment

To install OpenCV using conda: `conda install -c conda-forge opencv`

To reset camera: `sudo modprobe -r uvcvideo && sudo modprobe uvcvideo`

## Setting up the BeagleBone Green

I have a couple of BeagleBone Greens that I bought for another project. So that is what I will be using. Another single board computer like the Raspberry PI will probably work fine too.

First connect BBG to PC via USB. SSH to BBG as debian@192.168.7.2 default password is *temppwd*.

### Install OpenCV

Install OpenCV for Python 3 using 
```
$ sudo apt install python3-opencv
``` 
(this will take a while)

### Set timezone

The current time will be printed on the video, so we will want to see the correct timezone.

Check current timezone 
```
$ timedatectl
```

List available timezones 
```
$ timedatectl list-timezones
```

Set timezone 
```
$ sudo timedatectl set-timezone Australia/Brisbane
```

### Configure wireless

coming...

### Clone the project from GitHub

Configure Git
```
$ git config --global user.name "<name>" && git config --global user.email <email address> 
```

Clone the repository
```
$ git clone https://github.com/nielsenamrose/trap-camera.git
```

### Start the program processes when the device starts

```
$ sudo crontab -e
```

```
@reboot cd /home/debian/trap-camera && ./start.sh &
