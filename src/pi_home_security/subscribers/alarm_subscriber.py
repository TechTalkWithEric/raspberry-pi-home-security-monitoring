from pi_home_security.bus.event_bus import event_bus
from pi_home_security.hardware.models.security_device import SecurityDevice


@event_bus.subscriber("sensor.updated")
def alarm_event_listener(device: SecurityDevice):
    if not device:
        return

    if device.state == "open":
        print(f"🔔 Alarm triggered: {device.name} is OPEN")
        # Add actual alarm trigger logic here
    elif device.state == "closed":
        print(f"✅ Sensor closed: {device.name}")