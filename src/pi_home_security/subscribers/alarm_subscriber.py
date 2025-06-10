from typing import Dict, Any
from pi_home_security.bus.event_bus import event_bus
# from pi_home_security.hardware.models.security_device import SecurityDevice


@event_bus.subscriber("sensor.updated")
def alarm_event_listener(device: Dict[str, Any]):
    if not device:
        return

    if device.get("state") == "open":
        print(f"🔔 Alarm triggered: {device.get('name')} is OPEN")
        # Add actual alarm trigger logic here
    elif device.get("state")== "closed":
        print(f"✅ Sensor closed: {device.get('name')}")