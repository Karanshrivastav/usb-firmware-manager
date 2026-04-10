# tests/test_mock_data.py
from mock_data import MockUSBDeviceScanner, MockFirmwareRepository

def test_scan_returns_devices():
    devices = MockUSBDeviceScanner().scan()
    assert 4 <= len(devices) <= 8
    for d in devices:
        assert "name" in d and "vid" in d and "current_fw" in d

def test_firmware_versions_have_required_fields():
    repo = MockFirmwareRepository()
    versions = repo.get_versions("MCU-STM32F4")
    assert len(versions) > 0
    for fw in versions:
        assert "version" in fw and "release_date" in fw and "notes" in fw