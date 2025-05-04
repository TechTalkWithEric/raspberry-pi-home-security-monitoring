# PiBoard
from typing import Dict, Any
from pi_home_security.hardware.boards.pi_main_board import PiMainBoard
from pi_home_security.hardware.boards.extension_boards.pi_mcp23017_extension_board import PiMCP23017ExtensionBoard as PiExtensionBoard
from pi_home_security.hardware.gpio_service import GPIOService

class PiBoard:
    def __init__(self, use_extension=True):
        self.pi_board = PiMainBoard()
        # TODO: move this to a factory and load based on config
        self.ext_board = PiExtensionBoard() if use_extension else None

        self._pins: Dict[str, Any]= {**self.pi_board.pins, **self.ext_board.pins}
        if self.ext_board:
            self._pins.update(self.ext_board.pins)

        self.gpio_service: GPIOService= GPIOService()

    def get_pin(self, label: str):
        return self._pins.get(label)

    @property
    def pins(self):
        return self._pins
