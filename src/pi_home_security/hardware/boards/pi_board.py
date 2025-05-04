# PiBoard
from typing import Dict, Any
from pi_home_security.hardware.boards.pi_main_board import PiMainBoard
from pi_home_security.hardware.boards.extension_boards.pi_mcp23017_extension_board import PiMCP23017ExtensionBoard
from pi_home_security.hardware.gpio_service import GPIOService

class PiBoard:
    def __init__(self, use_extension=True):
        self._pins = {}
        self._pins.update(PiMainBoard().pins)
        if use_extension:
            self._pins.update(PiMCP23017ExtensionBoard().pins)

    @property
    def pins(self):
        return self._pins
