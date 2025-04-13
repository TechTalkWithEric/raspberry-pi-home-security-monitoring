from datetime import datetime
from pi_home_security.pi_pin import PiPin



class SecurityDevice:
    """
    A Security Device 
        Such as: window / door sensor, motion, camera, robot, etc
    
        NOTE: Currently we are mapping this to a Raspberry Pi GPIO pin.
        We're starting with door and window sensors but I'd like to make 
        it more genric in the future for expansion... time will tell how I
        make this work.

        For example our robot will will be registerd with our Pi for communication
        but it may not have a direct interface with a GPIO (PiPin) it may just be a 
        web / socket call or other communication piece.
    
    """
    def __init__(
        self,
        name: str,
        pi_pin: PiPin,
        location: str | None = None,
        type: str | None = None,
        state: str = "initialzing",
        zone: str | None = None,
    ):
        self.name: str = name
        self.location: str | None = location
        self.type: str | None = type  # motion, door, window, etc.
        self.__state: str = state  # open, closed, motion, etc.
        self.pin: PiPin = pi_pin
        self.zone: str | None = zone
        self.__last_updated: datetime = datetime.now()
        self.callbacks: list[callable] = []

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
        self.__last_updated = datetime.now()
        for callback in self.callbacks:
            callback(self)

    @property
    def last_updated(self):
        return self.__last_updated
