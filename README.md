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