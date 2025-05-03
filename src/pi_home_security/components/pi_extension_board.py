
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from pi_home_security.components.pi_pin import PiPin


class PiExtensionBoard:
    def __init__(self, address=0x20, i2c_bus=None):
        self.i2c = i2c_bus or busio.I2C(board.SCL, board.SDA)
        self.chip = MCP23017(self.i2c, address=address)
        self._pins = {}
        self._init_pins()

    def _init_pins(self):
        for pin_num in range(16):
            pin = self.chip.get_pin(pin_num)
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP

            label = f"EXT{pin_num:02d}"
            pi_pin = PiPin(bcm=label, board=label, name=f"MCP23017 Pin {pin_num}", external_pin=pin)
            self._pins[label] = pi_pin

    @property
    def pins(self):
        return self._pins
