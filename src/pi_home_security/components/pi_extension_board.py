import os
import glob
import digitalio
import busio
import board

from smbus2 import SMBus
from adafruit_mcp230xx.mcp23017 import MCP23017
from pi_home_security.components.pi_pin import PiPin


class PiExtensionBoard:
    def __init__(self, address=0x27, i2c_bus=None):
        self.address = address
        self.i2c_bus_number = self.find_i2c_bus(address) if i2c_bus is None else i2c_bus

        if self.i2c_bus_number is None:
            raise RuntimeError(f"MCP23017 not found at address 0x{address:02X} on any I2C bus.")

        # Open the I2C bus manually using busio and the chosen bus number        
        self.i2c = busio.I2C(scl=board.SCL, sda=board.SDA)

        self.chip = MCP23017(self.i2c, address=self.address)
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

    @staticmethod
    def find_i2c_bus(address, max_bus=20):
        """Search /dev/i2c-* for the given I2C address."""
        for dev in sorted(glob.glob("/dev/i2c-*")):
            try:
                bus_number = int(dev.rsplit("-")[-1])
                with SMBus(bus_number) as bus:
                    bus.read_byte(address)
                    return bus_number
            except Exception as e:
                print(e)
                continue
        return None


def main():
    board:PiExtensionBoard = PiExtensionBoard()



if __name__ == "__main__":
    main()