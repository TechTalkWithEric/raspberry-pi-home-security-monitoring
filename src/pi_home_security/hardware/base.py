

from abc import ABC, abstractmethod

class GPIOInterface(ABC):
    """
    Abstract base class for GPIO interfaces.
    Defines the common interface for interacting with GPIO pins.
    """
    
    @abstractmethod
    def setup_input(self, *args, **kwargs): ...
    
    @abstractmethod
    def setup_output(self, *args, **kwargs): ...

    @abstractmethod
    def read(self, *args) -> bool: ...

    @abstractmethod
    def write(self, *args, value: bool): ...

    @abstractmethod
    def cleanup(self): ...
