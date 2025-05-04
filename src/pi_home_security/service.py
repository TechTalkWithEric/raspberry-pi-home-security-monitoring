# Refactored HomeSecurityService to match updated GPIO architecture

import os
import json
from typing import Dict, Any, List
from signal import pause

from pi_home_security.hardware.boards.pi_board import PiBoard

from pi_home_security.hardware.gpiozero_impl import GPIOZeroService
from pi_home_security.hardware.gpio_service import GPIOService


class HomeSecurityService:
    def __init__(self):
        self.board: PiBoard | None = None
        self.gpio_service: GPIOService | None = None
        self._verbose: bool = True
        self.config: dict = {}
        self._load()

    def _load(self):
        self.board = PiBoard()
        self.gpio_service = GPIOService(GPIOZeroService(self.board.pins))

        self.__list_pins()
        self.__load_configuration()
        self.__run()

    def __list_pins(self):
        if not self._verbose:
            return

        for key, pin in self.board.pins.items():
            print(f"pin: {key} {pin.name}")

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
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON config: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def __load_security_sensors(self):
        sensors: List[Dict[str, Any]] = self.config.get("sensors", [])
        print("Activating sensors...")

        for sensor in sensors:
            pin_id = sensor.get("pin")
            gpio_type = sensor.get("input_type", "button")
            name = sensor.get("name")
            

            if pin_id not in self.board.pins:
                print(f"⚠️ Pin {pin_id} not found in board registry")
                continue

            self.gpio_service.setup_input(
                pin_id=pin_id,
                input_type=gpio_type,
                name=name,
                when_pressed=self.__on_sensor_triggered,
                when_released=self.__on_sensor_released
            )
            print(f"✅ Sensor loaded: {name} on {pin_id}")

    def __on_sensor_triggered(self, pin, name):
        print(f"🔔 {name} (pin {pin}) triggered")

    def __on_sensor_released(self, pin, name):
        print(f"✅ {name} (pin {pin}) released")

    def __run(self, mode: int = 0):
        if mode == 1:
            print("Attempting to recover from an unknown error.")

        print("🟢 Listening for sensor activity (Ctrl+C to exit)...")

        try:
            pause()
        except KeyboardInterrupt:
            response = input("Are you sure you want to exit [Y/n]?")
            if response.strip().lower() == "y":
                self.__exit()
                return
            self.__run(2)
        except Exception as e:
            print(f"Error: {e}\nRestarting service...")
            self.__run(1)

    def __exit(self):
        if self.gpio_service:
            self.gpio_service.cleanup()
        print("🚪 Shutting Down")


def main():
    HomeSecurityService()


if __name__ == "__main__":
    main()
