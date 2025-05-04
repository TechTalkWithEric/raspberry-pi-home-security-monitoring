# PiMCP23017ExtensionBoard
import board
import glob
import busio
import digitalio
from smbus2 import SMBus
from adafruit_mcp230xx.mcp23017 import MCP23017
from pi_home_security.components.pi_pin import PiPin

class PiMCP23017ExtensionBoard:
    def __init__(self, address=0x27):
        self.address = address
        self.i2c_bus_number = self.find_i2c_bus(address)
        if self.i2c_bus_number is None:
            raise RuntimeError(f"MCP23017 not found at 0x{address:02X}")
        self.i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
        self.chip = MCP23017(self.i2c, address=self.address)
        self._pins = {}
        self._init_pins()

    def _init_pins(self):
        for i in range(16):
            pin = self.chip.get_pin(i)
            pin.direction = digitalio.Direction.INPUT
            pin.pull = digitalio.Pull.UP
            label = f"EXT{i:02d}"
            self._pins[label] = PiPin(label, name=label, external_pin=pin)

    @property
    def pins(self):
        return self._pins

    @staticmethod
    def find_i2c_bus(address):
        for dev in sorted(glob.glob("/dev/i2c-*")):
            try:
                bus_number = int(dev.rsplit("-")[-1])
                with SMBus(bus_number) as bus:
                    bus.read_byte(address)
                    return bus_number
            except Exception:
                continue
        return None


def main():
    board:PiMCP23017ExtensionBoard = PiMCP23017ExtensionBoard()



if __name__ == "__main__":
    main()