# Facade / entrypoint

import os
from .base import GPIOInterface


class GPIOService(GPIOInterface):
    def __init__(self, backend: GPIOInterface):
        self.backend = backend

    def setup_input(self, *args, **kwargs):
        self.backend.setup_input(*args, **kwargs)

    def setup_output(self, *args, **kwargs):
        self.backend.setup_output(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.backend.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        self.backend.write(*args, **kwargs)

    def cleanup(self):
        self.backend.cleanup()
