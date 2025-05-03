# pi_home_security/components/composite_board.py

from pi_home_security.components.pi_main_board import PiMainBoard
from pi_home_security.components.pi_extension_board import PiExtensionBoard


class PiBoard:
    def __init__(self, use_extension=True):
        self.pi_board = PiMainBoard()
        self.ext_board = PiExtensionBoard() if use_extension else None

        self._pins = {**self.pi_board.gpio}
        if self.ext_board:
            self._pins.update(self.ext_board.pins)

    def get_pin(self, label: str):
        return self._pins.get(label)

    @property
    def all_pins(self):
        return self._pins
