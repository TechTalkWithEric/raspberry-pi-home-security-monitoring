from datetime import datetime
from typing import Callable, Optional
from pi_home_security.components.pi_pin import PiPin

class SecurityDevice:
    """
    Represents a physical or logical security device, such as a door sensor,
    motion detector, or WiFi-based device.
    """

    def __init__(
        self,
        name: str,
        sensor_type: str,
        zone: str = "",
        interface: Optional[object] = None,
    ):
        """
        Initialize a new SecurityDevice.

        Args:
            name (str): Display name for the device.
            sensor_type (str): Type of sensor (e.g., 'door', 'motion').
            zone (str): Optional zone name.
            interface (object): Optional hardware interface (e.g. PiPinInterface).
        """
        self.name = name
        self.sensor_type = sensor_type
        self.zone = zone
        self.interface = interface
        self.state = "initializing"
        self.last_updated = datetime.now()
        self.callbacks: list[Callable[[SecurityDevice], None]] = []

    def update_state(self, new_state: str) -> None:
        """
        Updates the internal state and notifies observers.

        Args:
            new_state (str): The new state (e.g. 'open', 'closed', 'motion')
        """
        self.state = new_state
        self.last_updated = datetime.now()
        for cb in self.callbacks:
            cb(self)

    def on_change(self, callback: Callable[['SecurityDevice'], None]) -> None:
        """
        Registers a callback that fires when the device's state changes.

        Args:
            callback (callable): A function that takes the device instance.
        """
        self.callbacks.append(callback)


class PiPinInterface:
    """
    Represents a GPIO-based interface for a Raspberry Pi pin (physical or expansion).
    """

    def __init__(self, pin_id: str, pin_obj: PiPin, is_external: bool):
        """
        Args:
            pin_id (str): The label or key used to identify the pin.
            pin_obj (object): The PiPin or MCP23017 Pin object.
            is_external (bool): Whether the pin is on an expansion board.
        """
        self.pin_id = pin_id
        self.pin_obj = pin_obj
        self.is_external = is_external