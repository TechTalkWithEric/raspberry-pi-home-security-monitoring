import threading
import time
from gpiozero import Button, LED, MotionSensor, DigitalOutputDevice
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory
from pi_home_security.components.pi_pin import PiPin
Device.pin_factory = LGPIOFactory()

class GPIOZeroService:
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

    def __init__(self, pin_registry: dict[str, PiPin]):
        self.pin_registry = pin_registry
        self.inputs = {}
        self.outputs = {}
        self.polling_threads = []

    def setup_input(self, pin_id: str, input_type="button", name=None, **kwargs):
        pin = self.pin_registry[pin_id]
        if pin.external_pin:
            self._setup_external_input(pin_id, pin, input_type, name, **kwargs)
        else:
            self._setup_pi_input(pin_id, pin, input_type, name, **kwargs)

    def _setup_pi_input(self, pin_id, pin, input_type, name, **kwargs):
        cls = self.INPUT_CLASSES[input_type]
        events = self.INPUT_EVENTS.get(input_type, [])
        event_handlers = {e: kwargs.pop(e, None) for e in events}

        device = cls(pin.bcm, **kwargs)
        self.inputs[pin_id] = device

        for event, handler in event_handlers.items():
            if handler:
                def wrapped(h=handler, label=pin_id, name=name):
                    return lambda: h(pin=label, name=name)
                setattr(device, event, wrapped())

    def _setup_external_input(self, pin_id, pin, input_type, name, **kwargs):
        device = pin.external_pin
        self.inputs[pin_id] = device

        when_pressed = kwargs.pop("when_pressed", None)
        when_released = kwargs.pop("when_released", None)

        def poll():
            last_state = device.value
            while True:
                time.sleep(0.25)
                current = device.value
                if current != last_state:
                    last_state = current
                    if current == 0 and when_pressed:
                        when_pressed(pin=pin_id, name=name)
                    elif current == 1 and when_released:
                        when_released(pin=pin_id, name=name)

        thread = threading.Thread(target=poll, daemon=True)
        thread.start()
        self.polling_threads.append(thread)

    def setup_output(self, pin_id: str, output_type="led", **kwargs):
        pin = self.pin_registry[pin_id]
        cls = self.OUTPUT_CLASSES[output_type]
        if pin.external_pin:
            raise NotImplementedError("Output to MCP23017 pins is not yet supported.")
        self.outputs[pin_id] = cls(pin.bcm, **kwargs)

    def read(self, pin_id: str) -> bool:
        device = self.inputs.get(pin_id)
        return device.value if hasattr(device, 'value') else False

    def write(self, pin_id: str, value: bool):
        device = self.outputs.get(pin_id)
        if device:
            device.on() if value else device.off()

    def cleanup(self):
        for d in list(self.inputs.values()) + list(self.outputs.values()):
            if hasattr(d, 'close'):
                d.close()
        self.inputs.clear()
        self.outputs.clear()
        self.polling_threads.clear()