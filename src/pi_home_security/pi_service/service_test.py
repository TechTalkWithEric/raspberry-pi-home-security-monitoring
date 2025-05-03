from gpiozero import Button, Device
from gpiozero.pins.lgpio import LGPIOFactory
from signal import pause

from pi_home_security.pi_service.service import GPIOService


# sensor list
# TODO: pull from a config file
SENSOR_CONFIGS= [
    {
        "pin": 17,
        "name": "Front Door",
        "type": "door"
    },
    {
        "pin": 18,
        "name": "Kitchen/Garage Door",
        "type": "door"
    },
    {
        "pin": 24,
        "name": "Kitchen/Deck Door",
        "type": "door"
    },
    {
        "pin": 25,
        "name": "GreatRoom Door",
        "type": "door"
    },
    {
        "pin": 23,
        "name": "Basement Outside Door",
        "type": "door"
    }
]



def on_door_opened(pin, name):
    print(f"👐 {name} (pin {pin}) opened!")

def on_door_closed(pin, name):
    print(f"🔒 {name} (pin {pin}) closed.")

serivce = GPIOService()

for item in SENSOR_CONFIGS:
    serivce.setup_input(
        pin=item.get("pin"),
        input_type=item.get("type"),
        name=item.get("name"),
        when_pressed=on_door_opened,
        when_released=on_door_closed
    )

print("🟢 Listening for sensor activity v2 (Ctrl+C to exit)...")
pause()
