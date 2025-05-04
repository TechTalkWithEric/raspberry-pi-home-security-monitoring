

from abc import ABC, abstractmethod

class GPIOInterface(ABC):
    """
    Abstract base class for GPIO interfaces.
    Defines the common interface for interacting with GPIO pins.
    """
    
    @abstractmethod
    def setup_input(self, controller: str, pin: int, input_type="button", name: str | None = None, **kwargs): ...
    
    @abstractmethod
    def setup_output(self, controller: str, pin: int, input_type="button", **kwargs): ...

    @abstractmethod
    def read(self, controller: str, pin: int) -> bool: ...

    @abstractmethod
    def write(self, controller: str, pin: int, value: bool): ...

    @abstractmethod
    def cleanup(self): ...
