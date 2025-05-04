
# PiMainBoard
from typing import Literal
from pi_home_security.components.pi_pin import PiPin



class PiMainBoard:
    def __init__(self):
        self._pins = {}
        self._init_pins()

    def _init_pins(self):
        mappings = [
            (2, "GPIO2"), (3, "GPIO3"), (4, "GPIO4"),
            (14, "TXD0"), (15, "RXD0"), (17, "GPIO17"),
            (18, "GPIO18"), (27, "GPIO27"), (22, "GPIO22"),
            (23, "GPIO23"), (24, "GPIO24"), (10, "MOSI"),
            (9, "MISO"), (25, "GPIO25"), (11, "SCLK"),
            (8, "CE0"), (7, "CE1"), (0, "ID_SD"),
            (1, "ID_SC"), (5, "GPIO5"), (6, "GPIO6"),
            (12, "GPIO12"), (13, "GPIO13"), (19, "GPIO19"),
            (16, "GPIO16"), (26, "GPIO26"), (20, "GPIO20"),
            (21, "GPIO21"),
        ]
        for bcm, name in mappings:
            self._pins[name] = PiPin(bcm, name=name)

    @property
    def pins(self):
        return self._pins
