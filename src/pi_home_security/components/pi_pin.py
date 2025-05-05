"""
RPi
"""
from typing import Any

class PiPin:
    def __init__(self, bcm: str | int, name: str | None=None, external_pin: Any=None):
        """
        A representation of Pi GPIO Pin
        Args:
            bcm (str | int): string or int (e.g., 17 or 'EXT03')
            name (str): friendly name or lable
            external_pin (Any): eg.g MCP23017 pin or None for native Pi
        """
        self.bcm = bcm                    
        self.name = name or str(bcm)     
        self.external_pin = external_pin 

    def __str__(self):
        return self.name or str(self.bcm)