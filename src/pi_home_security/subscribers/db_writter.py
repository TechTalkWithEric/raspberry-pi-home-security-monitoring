from pi_home_security.bus.event_bus import event_bus
from pi_home_security.hardware.models.security_device import SecurityDevice
from typing import Dict, Any

@event_bus.subscriber("sensor.updated")
def db_writer_event_listener(device: Dict[str, Any]):
    if not device:
        return

    if device.get("state")== "open":
        print(f"🛜 db write: {device.get('name')} is OPEN 👋")
        # Add actual alarm trigger logic here
    elif device.get("state") == "closed":
        print(f"🛜 db write: {device.get('name')} is CLOSED 🚪")