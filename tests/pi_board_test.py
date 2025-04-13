
import unittest
from pi_home_security.components.pi_board import PiBoard
from pi_home_security.components.pi_pin import PiPin

class TestPiBoard(unittest.TestCase):
    def test_gpio(self):
        pi = PiBoard()

        # Access GPIO 17 (BCM mode)
        pin: PiPin = pi.gpio[17]
        pin.mode = "IN"
        pin.state = 1
        print(pin)

        # Access physical pin 11 (BOARD mode)
        pin2 = pi.board[11]
        print(pin2)

        
        