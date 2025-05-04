
import unittest
from pi_home_security.hardware.gpio_service import GPIOService

class PiGPIOServiceTest(unittest.TestCase):

    def test_pi_zero(self):
        gpio = GPIOService()

        # Setup a button on pin 17 with pull-down resistor
        gpio.setup_input(pin=17, input_type="button", pull_up=False)

        # Setup a motion sensor
        gpio.setup_input(pin=27, input_type="motion")

        # Setup a digital output device (like a relay)
        gpio.setup_output(pin=22, output_type="digital", active_high=True)

        # Read and write
        if gpio.read(17):
            gpio.write(22, True)

