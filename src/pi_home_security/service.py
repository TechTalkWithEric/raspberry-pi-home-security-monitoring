import os
import json
from typing import Dict, Any, List
from signal import pause

from pi_home_security.hardware.boards.pi_board import PiBoard
from pi_home_security.components.pi_pin import PiPin
from pi_home_security.hardware.models.security_device import SecurityDevice, PiPinInterface
from pi_home_security.bus.event_bus import event_bus
from pi_home_security.subscribers import load_all_subscribers

class HomeSecurityService:
    def __init__(self):
        self.board: PiBoard | None = None
        self._verbose: bool = True
        self.config: dict = {}
        self.devices: Dict[str, SecurityDevice] = {}

        self._load()

    def _load(self):
        """Initializes system components."""
        self.board = PiBoard()
        self.__list_pins()
        self.__load_configuration()
        # load all of our subscriber
        load_all_subscribers()

        # always do this last... nothing else runs after it
        self.__run()
        

    def __list_pins(self):
        if not self._verbose:
            return

        pins: Dict[str, Any] = self.board.pins
        for key, pi_pin in pins.items():
            print(f"pin: {key} {pi_pin.name}")

    def __load_configuration(self):
        file = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(file):
            print("🚫 No Config Found... there is nothing to monitor")
            return

        config = self.load_json(file)
        if config:
            self.config = config

        self.__load_security_sensors()

    def load_json(self, filepath: str) -> dict | None:
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None

    def __load_security_sensors(self):
        sensors: List[Dict[str, Any]] = self.config.get("sensors", [])
        print("Activating sensors...")

        for sensor in sensors:
            name = sensor.get("name")
            pin = str(sensor.get("pin"))
            input_type = sensor.get("sensor_type", "button")
            controller = sensor.get("gpio_controller", "pi").lower()

            pi_pin: PiPin = self.board.pins.get(pin)
            if not pi_pin:
                print(f"Skipping unknown pin: {pin}")
                continue

            interface = PiPinInterface(pin_id=pin, pin_obj=pi_pin, is_external=controller != "pi")
            device = SecurityDevice(name=name, sensor_type=input_type, interface=interface)

            device.on_change(lambda d: self.handle_sensor_event(d))
            self.board.gpio_service.setup_input(device, input_type)
            self.devices[pin] = device

    def handle_sensor_event(self, device: SecurityDevice):
        print(f"[ALERT] {device.name} changed to {device.state.upper()} at {device.last_updated}")
        event_bus.publish("sensor.updated", device)

    def __run(self, mode: int = 0):
        if mode == 1:
            print("Attempting to recover from an unknown error.")

        print("🟢 Listening for sensor activity (Ctrl+C to exit)...")

        try:
            pause()
        except KeyboardInterrupt:
            response = input("Are you sure you want to exit [Y/n]?")
            if response.lower() == "y":
                self.__exit()
            else:
                self.__run(2)
        except Exception as e:
            print(f"[ERROR] {e}")
            self.__run(1)

    def __exit(self):
        print("🚪 Shutting Down")
        if self.board:
            self.board.gpio_service.cleanup()


def main():
    HomeSecurityService()


if __name__ == "__main__":
    main()
