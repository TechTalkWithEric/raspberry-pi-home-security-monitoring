# Facade / entrypoint

import os
from .gpiozero_impl import GPIOZeroService
from .mock_impl import MockGPIOService
from .base import GPIOInterface
# from .pigpio_impl import PiGPIOService  # Optional

class GPIOService(GPIOInterface):
    def __init__(self):
        self.service = get_gpio_service()

    def setup_input(self, pin: int, input_type="button", **kwargs):
        self.service.setup_input(pin, input_type=input_type, **kwargs)

    def setup_output(self, pin: int, input_type="button", **kwargs):
        self.service.setup_output(pin, input_type=input_type, **kwargs)

    def read(self, pin: int) -> bool:
        return self.service.read(pin)

    def write(self, pin: int, value: bool):
        self.service.write(pin, value)

    def cleanup(self):
        self.service.cleanup()

def get_gpio_service() -> 'GPIOInterface':
    if os.uname().sysname == "Linux":
        return GPIOZeroService()
    else:
        return MockGPIOService()
