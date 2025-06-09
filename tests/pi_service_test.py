import os
import json
import pytest
from unittest.mock import MagicMock, patch

import pi_home_security.subscribers as subscribers
from pi_home_security.hardware.models.security_device import SecurityDevice
from pi_home_security.hardware.boards.pi_board import PiBoard
from pi_home_security.bus.event_bus import event_bus
from pi_home_security.service import HomeSecurityService

# Sample dummy pin object
class DummyPin:
    def __init__(self, label):
        self.label = label
        self.value = False
        self.name = f"Name-{label}"

@pytest.fixture(autouse=True)
def no_subscribers(monkeypatch):
    # Prevent real subscribers from loading
    monkeypatch.setattr(subscribers, 'load_all_subscribers', lambda: None)
    yield

@pytest.fixture
def dummy_board(monkeypatch):
    # Prepare dummy pins
    pins = {"GPIO17": DummyPin("GPIO17"), "EXT01": DummyPin("EXT01")}

    # Fake PiBoard __init__ to set pins and gpio_service
    def fake_init(self):
        self.pins = pins
        self.gpio_service = MagicMock()
    monkeypatch.setattr(PiBoard, '__init__', fake_init)

    # Return instantiated fake board
    return PiBoard()

@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    # Write a valid config.json fixture
    config_data = {
        "sensors": [
            {"name": "Front Door", "pin": "GPIO17", "gpio_controller": "pi", "sensor_type": "button"},
            {"name": "Office Door", "pin": "EXT01", "gpio_controller": "mcp23017", "sensor_type": "button"}
        ]
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    # Patch path resolution so HomeSecurityService finds our fixture
    monkeypatch.setenv('CONFIG_DIR', str(tmp_path))
    monkeypatch.setattr(os.path, 'dirname', lambda _: str(tmp_path))
    return config_data

# Tests for load_json

def test_load_json_success(tmp_path):
    filepath = tmp_path / "good.json"
    obj = {"key": "value"}
    filepath.write_text(json.dumps(obj))
    svc = HomeSecurityService.__new__(HomeSecurityService)
    result = svc.load_json(str(filepath))
    assert result == obj


def test_load_json_failure(tmp_path, capsys):
    filepath = tmp_path / "bad.json"
    svc = HomeSecurityService.__new__(HomeSecurityService)
    result = svc.load_json(str(filepath))
    captured = capsys.readouterr()
    assert result is None
    assert "Error loading" in captured.out

# Test configuration loading and sensor setup

def test_load_configuration_and_sensors(dummy_board, tmp_config, monkeypatch):
    svc = HomeSecurityService.__new__(HomeSecurityService)
    svc._verbose = False
    svc.board = dummy_board
    svc.config = {}
    svc.devices = {}

    # Invoke private load configuration
    HomeSecurityService._HomeSecurityService__load_configuration(svc)

    # Sensors should be loaded for GPIO17 and EXT01
    assert "GPIO17" in svc.devices
    assert svc.devices["GPIO17"].name == "Front Door"
    assert "EXT01" in svc.devices
    assert svc.devices["EXT01"].name == "Office Door"
    # gpio_service.setup_input should have been called twice
    assert dummy_board.gpio_service.setup_input.call_count == 2

# Test event publishing
@patch.object(event_bus, 'publish')
def test_handle_sensor_event(mock_publish):
    svc = HomeSecurityService.__new__(HomeSecurityService)
    device = MagicMock(spec=SecurityDevice)
    device.name = "Test"
    device.state = "open"
    device.last_updated = "now"

    svc.handle_sensor_event(device)
    mock_publish.assert_called_once_with("sensor.updated", device)
