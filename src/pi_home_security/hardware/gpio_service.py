# Facade / entrypoint

import os
from .gpiozero_impl import GPIOZeroService
from .mock_impl import MockGPIOService
from .base import GPIOInterface


class GPIOService(GPIOInterface):
    def __init__(self):
        self.services = {
            "pi": GPIOZeroService(),
            "mcp23017": GPIOZeroService(extension_board=True),
            "mock": MockGPIOService()
            # could support others like "mock" or "remote" later
        }

    def _get_service(self, controller: str) -> GPIOInterface:
        return self.services.get(controller)
    
    def setup_input(self, controller: str, pin: int, input_type="button", name: str | None = None, **kwargs):
        self._get_service(controller=controller).setup_input(pin, input_type=input_type, name=name, **kwargs)

    def setup_output(self,controller: str, pin: int, output_type="led", **kwargs):
        self._get_service(controller=controller).setup_output(pin, output_type=output_type, **kwargs)

    def read(self, controller: str,pin: int) -> bool:
        return self._get_service(controller=controller).read(pin)

    def write(self, controller: str,pin: int, value: bool):
        self._get_service(controller=controller).write(pin, value)

    def cleanup(self):
        for service in self.services.values():
            service.cleanup()

def get_gpio_service() -> 'GPIOInterface':
    if os.uname().sysname == "Linux":
        return GPIOZeroService()
    else:
        return MockGPIOService()
