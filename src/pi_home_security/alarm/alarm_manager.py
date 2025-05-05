import time
from enum import Enum
from typing import Dict


class AlarmState(Enum):
    DISARMED = "disarmed"
    ARMED_HOME = "armed_home"
    ARMED_AWAY = "armed_away"
    TRIGGERED = "triggered"


class AlarmManager:
    def __init__(self):
        self.state = AlarmState.DISARMED
        self.sensor_states: Dict[str, Dict[str, any]] = {}
        self._bypassed: set[str] = set()

    def update_sensor(self, pin: str, name: str, value: bool):
        state = "closed" if value else "open"
        state = {
            "pin": pin,
            "state": state,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(state)
        self.sensor_states[name] = state

        if self.state in [AlarmState.ARMED_HOME, AlarmState.ARMED_AWAY]:
            if name not in self._bypassed and state == "open":
                self._handle_alarm_trigger(name)

    def _handle_alarm_trigger(self, name: str):
        print("\n🚨🚨🚨 ALARM TRIGGERED 🚨🚨🚨")
        print(f"Triggered by: {name}")
        print("Taking necessary actions...")
        self.state = AlarmState.TRIGGERED
        # TODO: Sound buzzer, send notification, etc.

    def arm(self, mode: str):
        try:
            self.state = AlarmState[mode.upper()]
            print(f"🔒 Alarm armed ({self.state.value})")
        except KeyError:
            print(f"Invalid alarm mode: {mode}")

    def disarm(self):
        self.state = AlarmState.DISARMED
        print("🔓 Alarm disarmed")

    def bypass(self, name: str):
        self._bypassed.add(name)
        print(f"Bypassed sensor: {name}")

    def status(self):
        print(f"\n📋 Alarm State: {self.state.value.upper()}")
        for name, data in self.sensor_states.items():
            bypassed = " (bypassed)" if name in self._bypassed else ""
            print(f"- {name}: {data['state']} @ {data['time']}{bypassed}")

    def reset(self):
        self._bypassed.clear()
        self.sensor_states.clear()
        self.state = AlarmState.DISARMED
        print("🔄 Alarm system reset")
