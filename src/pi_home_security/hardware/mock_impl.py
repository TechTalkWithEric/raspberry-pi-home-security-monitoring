# macOS-friendly mock implementation

from .base import GPIOInterface

class MockGPIOService(GPIOInterface):
    def __init__(self):
        self.state = {}

    def setup_input(self, pin: int, input_type="button", **kwargs):
        self.state[pin] = False

    def setup_output(self, pin: int, output_type="button", **kwargs):
        self.state[pin] = False

    def read(self, pin: int) -> bool:
        return self.state.get(pin, False)

    def write(self, pin: int, value: bool):
        self.state[pin] = value

    def cleanup(self):
        self.state.clear()
