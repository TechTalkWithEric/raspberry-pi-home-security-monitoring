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






## Pi Setup

In addition to adding this python code you will need to make sure some of the underlying services are installed as well.


### Pi0-Pi 5 Compatabilty Libraries
To make this compatibale with Pi 5 I'm using lgpio, this is a system wide library
and is not installed with pip (however `lgpio` is a pip library that needs to be installed).

Install this on the raspberry pi device
```sh
sudo apt install lgpio python3-lgpio

```


## Future Enhancements

Add support for Ring Actions / Notifications
- https://github.com/python-ring-doorbell/python-ring-doorbell

Add IoT MQTT Support (send events to AWS for longterm monitoring and actions)
- https://docs.aws.amazon.com/iot/latest/developerguide
- Store the data in DynamoDB
