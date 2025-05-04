# gpiozero-based implementation

from gpiozero import Button, LED, MotionSensor, DigitalOutputDevice
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

from .base import GPIOInterface
from pi_home_security.components.pi_pin import PiPin

# setup the pin factory
Device.pin_factory = LGPIOFactory()

class GPIOZeroService(GPIOInterface):
    # Default input/output type mappings
    INPUT_CLASSES = {
        "switch": Button,
        "button": Button,
        "door_sensor": Button,
        "door": Button,
        "window_sensor": Button,
        "window": Button,
        "motion": MotionSensor
    }
    # Maps input_type → supported event attributes
    INPUT_EVENTS = {
        "door_sensor": ["when_pressed", "when_released"],
        "door": ["when_pressed", "when_released"],
        "window_sensor": ["when_pressed", "when_released"],
        "window": ["when_pressed", "when_released"],
        "button": ["when_pressed", "when_released", "when_held"],
        "motion": ["when_motion", "when_no_motion"]
    }

    OUTPUT_CLASSES = {
        "led": LED,
        "digital": DigitalOutputDevice,
    }

    def __init__(self):
        self.inputs = {}   # pin: instance
        self.outputs = {}  # pin: instance

    def setup_input(self, pin: int, input_type="button", name=None, **kwargs):
        cls = self.INPUT_CLASSES.get(input_type)
        if not cls:
            raise ValueError(f"Unsupported input type: {input_type}")

        # Optional device name for identification
        name = name or f"{input_type}_{pin}"

        # Get valid events for this input type
        valid_events = self.INPUT_EVENTS.get(input_type, [])

        # Pull event handlers out of kwargs
        event_handlers = {
            event: kwargs.pop(event, None)
            for event in valid_events
        }

        device = cls(pin, **kwargs)
        self.inputs[pin] = device

        # Wrap and assign event handlers
        for event, handler in event_handlers.items():
            if handler:
                def wrapped_handler(handler=handler, pin=pin, name=name):
                    return lambda: handler(pin=pin, name=name)
                setattr(device, event, wrapped_handler())

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
