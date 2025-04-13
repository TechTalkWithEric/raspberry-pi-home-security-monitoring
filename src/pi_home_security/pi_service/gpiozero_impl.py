# gpiozero-based implementation

from gpiozero import Button, LED, MotionSensor, DigitalOutputDevice
from .base import GPIOInterface


class GPIOZeroService(GPIOInterface):
    # Default input/output type mappings
    INPUT_CLASSES = {
        "switch": Button,
        "button": Button,
        "door_sensor": Button,
        "window_sensor": Button,
        "motion": MotionSensor
    }

    OUTPUT_CLASSES = {
        "led": LED,
        "digital": DigitalOutputDevice,
    }

    def __init__(self):
        self.inputs = {}   # pin: instance
        self.outputs = {}  # pin: instance

    def setup_input(self, pin: int, input_type="button", **kwargs):
        cls = self.INPUT_CLASSES.get(input_type)
        if not cls:
            raise ValueError(f"Unsupported input type: {input_type}")
        self.inputs[pin] = cls(pin, **kwargs)

    def setup_output(self, pin: int, output_type="led", **kwargs):
        cls = self.OUTPUT_CLASSES.get(output_type)
        if not cls:
            raise ValueError(f"Unsupported output type: {output_type}")
        self.outputs[pin] = cls(pin, **kwargs)

    def read(self, pin: int) -> bool:
        device = self.inputs.get(pin)
        if hasattr(device, 'is_active'):
            return device.is_active
        raise ValueError(f"Device on pin {pin} has no readable state")

    def write(self, pin: int, value: bool):
        device = self.outputs.get(pin)
        if not device:
            raise ValueError(f"No output device configured on pin {pin}")
        device.on() if value else device.off()

    def cleanup(self):
        for device in list(self.inputs.values()) + list(self.outputs.values()):
            if hasattr(device, 'close'):
                device.close()
        self.inputs.clear()
        self.outputs.clear()
