import os
import json
from typing import Dict, Any, List
from signal import pause
from pi_home_security.hardware.boards.pi_board import PiBoard
from pi_home_security.components.pi_pin import PiPin
class HomeSecurityService:
    def __init__(self):        
        self.board: PiBoard | None = None
        self._verbose: bool = True
        self.config: dict = {}
        self._load()
        
    def _load(self):
        """Loads the sytem"""
        # load the pi board
        self.board: PiBoard = PiBoard()
                                
        self.__list_pins()
        # load the configuration
        self.__load_configuration()

        self.__run()

    def __list_pins(self):
        if not self._verbose:
            return
        
        pins: Dict[str, Any] = self.board.pins
        pi_pin: PiPin
        for key, pi_pin in pins.items():
            print(f"pin: {key} {pi_pin.name}")

    def __load_configuration(self):
        # TODO: 
        directory = os.path.dirname(__file__)
        file = os.path.join(directory, "config.json")
        if not os.path.exists(file):
            print("🚫 No Config Found... there is nothing to monitor")
            return
        

        config = self.load_json(file)
        if config:
            self.config = config

        self.__load_security_sensors()
        # 
    
    def load_json(self, filepath: str)-> dict | None:
        """Loads JSON data from a file.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            dict: A dictionary containing the data loaded from the JSON file.
                Returns None if an error occurs during file reading or JSON parsing.
        """
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in: {filepath}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    def __load_security_sensors(self):
        sensors: List[Dict[str, Any]] = self.config.get("sensors", [])
        print("activing sensors")

        sensor: Dict[str, Any]
        for sensor in sensors:
            gpio_controller = str(sensor.get("gpio_controller")).lower()
            if  gpio_controller== "pi":
                print("loading pi pin")
            elif gpio_controller == "mcp23017":
                print("loading mcp23017 pin")
            else:
                print("🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨")
                print(f"WARNING: Unknown gpio_controller: {gpio_controller}")
                print("WARNING: Nothing is being montiored for this sendor configuration!")
                print(sensor)
                print("🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨")
                print("")
                

    def __run(self, mode: int = 0):
        """Run the system"""
        if mode ==1:
            print("Attempting to recover from an unknown error.")

        print("🟢 Listening for sensor activity v2 (Ctrl+C to exit)...")

        try:
            pause()
        except KeyboardInterrupt as e:
            response = input("Are you sure you want to exit [Y/n]?")
            if str(response).lower() == "y":
                self.__exit()
                return
            else:
                self.__run(2)
                return
        except Exception as e:
            print("Unknown Error")
            print(str(e))
            print("Attempting to start backup.")

        # lets' run it again
        self.__run(1)

    def __exit(self):
        print("🚪 Shutting Down")



def main():
    service: HomeSecurityService = HomeSecurityService()


if __name__ == "__main__":
    main()