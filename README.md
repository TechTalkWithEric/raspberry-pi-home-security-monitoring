# raspberry-pi-home-security-monitoring
A home security monitoring app for raspberry pi


This is going to be my attempt to connect a raspberry pi to a window, door and motion sensors.


## Troubleshooting

Having issues with TK?

```sh
import _tkinter # If this fails your Python may not be configured for Tk
```



### Mac OS
This one helped me.

- [Stackoverflow](https://stackoverflow.com/questions/22550068/python-not-configured-for-tk)

```sh

brew uninstall pyenv && rm -rf ~/.pyenv.
# add it back
brew update
brew install zlib
brew install tcl-tk 
brew install pyenv

```


## Future

Add support for Ring Actions / Notifications
- https://github.com/python-ring-doorbell/python-ring-doorbell



## Pi Setup

In addition to adding this python code you will need to make sure some of the underlying services are installed as well.

```sh
# install the services
sudo apt update
sudo apt install pigpio python3-pigpio

# start the services
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# verfiy
sudo systemctl status pigpiod

```

## Staus Failures

`“This system does not appear to be a Raspberry Pi.”`
The package may not be Pi5 ready

```sh
sudo apt remove pigpio

cd ~
git clone https://github.com/joan2937/pigpio.git
cd pigpio
make
sudo make install

# start the service
sudo pigpiod

sudo systemctl status pigpiod
```


sudo apt remove pigpio 
sudo apt remove python3-pigpio

# Pi0-Pi 5 Compatabilty Libraries
To make this compatibale with Pi 5 I'm using lgpio, this is a system wide library
and is not installed with pip.

```sh
sudo apt install lgpio python3-lgpio

```
