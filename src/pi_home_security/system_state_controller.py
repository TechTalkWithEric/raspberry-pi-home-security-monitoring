# state_controller.py
from typing import Dict, Any
from pi_home_security.bus.event_bus import event_bus
from pi_home_security.hardware.models.security_device import SecurityDevice

class SystemStateController:
    def __init__(self):
        self.armed: bool = False
        self.bypassed_sensors: set[str] = set()

        # Subscribe to raw sensor events and user commands
        event_bus.subscribe("sensor.raw",   self._on_sensor_raw)
        event_bus.subscribe("system.arm",   self._on_arm_command)
        event_bus.subscribe("system.disarm",self._on_disarm_command)
        event_bus.subscribe("system.bypass",self._on_bypass_command)

    def _on_arm_command(self, payload):
        self.armed = True
        event_bus.publish("system.state_changed", {"armed": True})

    def _on_disarm_command(self, payload):
        self.armed = False
        event_bus.publish("system.state_changed", {"armed": False})

    def _on_bypass_command(self, payload):
        sensor_id = payload["sensor_id"]
        if payload.get("bypass", True):
            self.bypassed_sensors.add(sensor_id)
        else:
            self.bypassed_sensors.discard(sensor_id)
        event_bus.publish("system.state_changed", {
            "bypassed_sensors": list(self.bypassed_sensors)
        })

    def _on_sensor_raw(self, payload: Dict[str, Any]):
        sensor_id = payload.get("device_id") or payload.get("id")
        # enrich the payload for downstream subscribers:
        enriched = {
          **payload,
          "armed": self.armed,
          "bypassed": sensor_id in self.bypassed_sensors
        }

        print(f"enriched meta data")
        print(f"👉 {enriched}")

        event_bus.publish("sensor.updated", enriched)
