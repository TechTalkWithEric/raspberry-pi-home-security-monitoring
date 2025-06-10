import threading
import time
from typing import Dict, cast
from gpiozero import Button, LED, MotionSensor, DigitalOutputDevice
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
from pi_home_security.hardware.models.security_device import SecurityDevice, PiPinInterface
from pi_home_security.components.pi_pin import PiPin


Device.pin_factory = LGPIOFactory()


class GPIOZeroService:
    """
    GPIOZero-based input/output service for managing physical GPIO pins.
    Supports internal and external (e.g., MCP23017) pin handling.
    Manages all polling for the events
    """

    INPUT_CLASSES = {
        "button": Button, "door": Button, "window": Button, "motion": MotionSensor
    }
    INPUT_EVENTS = {
        "button": ["when_pressed", "when_released"],
        "door": ["when_pressed", "when_released"],
        "window": ["when_pressed", "when_released"],
        "motion": ["when_motion", "when_no_motion"]
    }
    OUTPUT_CLASSES = {
        "led": LED, "digital": DigitalOutputDevice,
    }

    def __init__(self, pin_registry: Dict[str, object]):
        """
        Args:
            pin_registry (dict): A dictionary mapping pin labels to PiPin objects.
        """
        self.pin_registry = pin_registry
        self.inputs: Dict[str, object] = {}
        self.outputs: Dict[str, object] = {}
        self.polling_threads = []

    def setup_input(self, device: SecurityDevice, input_type: str = "button") -> None:
        """
        Configures an input device and links it to the SecurityDevice.

        Args:
            device (SecurityDevice): The security device to monitor.
            input_type (str): Type of GPIO input ('door', 'motion', etc.)
        """

        device_interface: PiPinInterface = cast(PiPinInterface, device.interface)
        pin = device_interface.pin_obj
        pin_id = device_interface.pin_id

        if device_interface.is_external:
            self._setup_external_input(device, pin_id, pin, input_type)
        else:
            self._setup_pi_input(device, pin_id, pin, input_type)

    def _setup_pi_input(self, device: SecurityDevice, pin_id: str, pin: PiPin, input_type: str):
        cls = self.INPUT_CLASSES[input_type]
        events = self.INPUT_EVENTS.get(input_type, [])

        device_obj = cls(pin.bcm)
        self.inputs[pin_id] = device_obj

        if "when_pressed" in events:
            device_obj.when_pressed = lambda: device.update_state("closed")
        if "when_released" in events:
            device_obj.when_released = lambda: device.update_state("open")

    def _setup_external_input(self, device: SecurityDevice, pin_id: str, pin: PiPin, input_type: str):
        gpio_pin = pin.external_pin  # The actual MCP23017 DigitalInOut object
        self.inputs[pin_id] = gpio_pin

        def poll():
            last_state = gpio_pin.value
            device.update_state("closed" if last_state == 0 else "open")

            while True:
                time.sleep(0.25)
                current = gpio_pin.value
                if current != last_state:
                    last_state = current
                    new_state = "closed" if current == 0 else "open"
                    device.update_state(new_state)

        thread = threading.Thread(target=poll, daemon=True)
        thread.start()
        self.polling_threads.append(thread)

    def setup_output(self, pin_id: str, output_type: str = "led", **kwargs) -> None:
        pin = self.pin_registry[pin_id]
        cls = self.OUTPUT_CLASSES[output_type]
        if pin.external_pin:
            raise NotImplementedError("Output to MCP23017 pins is not yet supported.")
        self.outputs[pin_id] = cls(pin.bcm, **kwargs)

    def read(self, pin_id: str) -> bool:
        device = self.inputs.get(pin_id)
        return device.value if hasattr(device, 'value') else False

    def write(self, pin_id: str, value: bool) -> None:
        device = self.outputs.get(pin_id)
        if device:
            device.on() if value else device.off()

    def cleanup(self) -> None:
        for d in list(self.inputs.values()) + list(self.outputs.values()):
            if hasattr(d, 'close'):
                d.close()
        self.inputs.clear()
        self.outputs.clear()
        self.polling_threads.clear()
