from gpiozero import Button, Device
from gpiozero.pins.lgpio import LGPIOFactory
from signal import pause

# Use the LGPIO factory for Raspberry Pi 5 compatibility
Device.pin_factory = LGPIOFactory()

# List of (pin, name) tuples
SENSOR_CONFIG = [
    (17, "Front Door"),
    (18, "Kitchen Door"),
    (24, "Breakfast Door"),
    (25, "Porch Door"),
    (23, "Basement Door"),
]

# Store Button objects
sensors = []

def make_handlers(name):
    def on_open():
        print(f"🔓 {name} opened! 🚨")
    def on_close():
        print(f"🔒 {name} closed! ✅")
    return on_open, on_close

# Initialize sensors and assign handlers
for pin, name in SENSOR_CONFIG:
    sensor = Button(pin, pull_up=True)
    on_open, on_close = make_handlers(name)
    sensor.when_pressed = on_close
    sensor.when_released = on_open
    sensors.append(sensor)

print("🟢 Listening for sensor activity (Ctrl+C to exit)...")
pause()
