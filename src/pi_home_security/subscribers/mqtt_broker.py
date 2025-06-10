from pi_home_security.bus.event_bus import event_bus
from pi_home_security.hardware.models.security_device import SecurityDevice
from typing import Dict, Any

@event_bus.subscriber("sensor.updated")
def mqtt_event_listener(device: Dict[str, Any]):
    if not device:
        return

    if device.get("state") == "open":
        print(f"🤖 broker state triggered: {device.get('name')} is OPEN 👋")
        # Add actual alarm trigger logic here
    elif device.get("state") == "closed":
        print(f"🤖 broker state triggered: {device.get('name')} is CLOSED 🚪")

    # import paho.mqtt.client as mqtt
    import json

    # client = mqtt.Client()
    # client.connect("localhost", 1883)

    # publish sensor event
    event = {
        "pin": device.get("name"),
        "state": device.get("state"),
        "datetime": device.get("last_updated"),
    }
    print(f"publishing {event}")
    # client.publish("home/security/sensor", json.dumps(event), qos=1)
