
from pi_home_security.components.pi_pin import PiPin



class PiBoard:
    """
    A Raspberry Pi Virtual Board
    
    """
    def __init__(self, mode="BCM"):
        self.mode = mode.upper()
        self._pins_by_bcm = {}
        self._pins_by_board = {}
        self._init_pins()

    def _init_pins(self):
        # Mapping of BCM, BOARD, name
        mappings = [
            (2, 3, "SDA1"), (3, 5, "SCL1"), (4, 7, "GPIO4"),
            (14, 8, "TXD0"), (15, 10, "RXD0"),
            (17, 11, "GPIO17"), (18, 12, "GPIO18"),
            (27, 13, "GPIO27"), (22, 15, "GPIO22"),
            (23, 16, "GPIO23"), (24, 18, "GPIO24"),
            (10, 19, "MOSI"), (9, 21, "MISO"),
            (25, 22, "GPIO25"), (11, 23, "SCLK"),
            (8, 24, "CE0"), (7, 26, "CE1"),
            (0, 27, "ID_SD"), (1, 28, "ID_SC"),
            (5, 29, "GPIO5"), (6, 31, "GPIO6"),
            (12, 32, "GPIO12"), (13, 33, "GPIO13"),
            (19, 35, "GPIO19"), (16, 36, "GPIO16"),
            (26, 37, "GPIO26"), (20, 38, "GPIO20"),
            (21, 40, "GPIO21"),
        ]

        for bcm, board, name in mappings:
            pin = PiPin(bcm, board, name)
            self._pins_by_bcm[bcm] = pin
            self._pins_by_board[board] = pin

    @property
    def gpio(self):
        return self._pins_by_bcm

    @property
    def board(self):
        return self._pins_by_board
