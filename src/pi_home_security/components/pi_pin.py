"""
RPi
"""
from typing import Literal

class PiPin:
    def __init__(self, bcm, name=None, external_pin=None):
        self.bcm = bcm                    # string or int (e.g., 17 or 'EXT03')
        self.name = name or str(bcm)     # friendly label
        self.external_pin = external_pin # MCP23017 pin or None for native Pi

    def __str__(self):
        return self.name or str(self.bcm)