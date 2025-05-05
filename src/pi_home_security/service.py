import os
import json
from typing import Dict, Any, List
from signal import pause
from pi_home_security.hardware.boards.pi_board import PiBoard
from pi_home_security.components.pi_pin import PiPin
from pi_home_security.alarm.alarm_manager import AlarmManager

class HomeSecurityService:
    def __init__(self):        
        self.board: PiBoard | None = None
        self._verbose: bool = True
        self.config: dict = {}
        self.alarm: AlarmManager = AlarmManager()
        self._load()

    def _load(self):
        self.board = PiBoard()
        self.__list_pins()
        self.__load_configuration()
        self.__run()

    def __list_pins(self):
        if not self._verbose:
            return
        for key, pi_pin in self.board.pins.items():
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

    def load_json(self, filepath: str)-> dict | None:
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None

    def __load_security_sensors(self):
        sensors: List[Dict[str, Any]] = self.config.get("sensors", [])
        print("Activating sensors...")

        def sensor_handler(pin: str, name: str):
            value = self.board.gpio_service.read(pin)
            self.alarm.update_sensor(pin, name, value)

        for sensor in sensors:
            name = sensor.get("name")
            pin = str(sensor.get("pin"))            
            input_type = sensor.get("sensor_type", "button")

            self.board.gpio_service.setup_input(
                pin_id=pin,
                input_type=input_type,
                name=name,
                when_pressed=sensor_handler,
                when_released=sensor_handler
            )

    def __run(self, mode: int = 0):
        if mode == 1:
            print("Recovering from an unknown error.")
        print("🟢 Listening for sensor activity (Ctrl+C to exit)...")

        try:
            pause()
        except KeyboardInterrupt:
            if input("Are you sure you want to exit [Y/n]?").lower() == "y":
                self.__exit()
            else:
                self.__run(2)
        except Exception as e:
            print(f"Unknown error: {e}")
            self.__run(1)

    def __exit(self):
        print("🚪 Shutting Down")
        self.board.gpio_service.cleanup()


def main():
    HomeSecurityService()


if __name__ == "__main__":
    main()