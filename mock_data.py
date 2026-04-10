"""
mock_data.py
─────────────────────────────────────────────────────────────────────────────
Simulates a USB device scanner and a firmware version repository.
In a production system these would talk to:
  • libusb / pyusb  – for real USB enumeration
  • A firmware CDN or S3 bucket  – for real version manifests
─────────────────────────────────────────────────────────────────────────────
"""

import random


# ── Raw device catalogue ──────────────────────────────────────────────────

_DEVICE_CATALOGUE = [
    {
        "product_id": "MCU-STM32F4",
        "name":       "STM32F4 Discovery Board",
        "vendor":     "STMicroelectronics",
        "type":       "Microcontroller",
        "vid":        "0483",
        "pid":        "374B",
    },
    {
        "product_id": "MCU-ARDUINO-MEGA",
        "name":       "Arduino Mega 2560",
        "vendor":     "Arduino LLC",
        "type":       "Microcontroller",
        "vid":        "2341",
        "pid":        "0042",
    },
    {
        "product_id": "AUDIO-FOCUSRITE-2I2",
        "name":       "Focusrite Scarlett 2i2",
        "vendor":     "Focusrite",
        "type":       "Audio",
        "vid":        "1235",
        "pid":        "8204",
    },
    {
        "product_id": "STORAGE-SANDISK-EXTREME",
        "name":       "SanDisk Extreme SSD",
        "vendor":     "SanDisk",
        "type":       "Storage",
        "vid":        "0781",
        "pid":        "5567",
    },
    {
        "product_id": "INPUT-CORSAIR-K95",
        "name":       "Corsair K95 RGB Platinum",
        "vendor":     "Corsair",
        "type":       "Input",
        "vid":        "1B1C",
        "pid":        "1B2D",
    },
    {
        "product_id": "CAM-LOGITECH-BRIO",
        "name":       "Logitech Brio 4K Pro",
        "vendor":     "Logitech",
        "type":       "Camera",
        "vid":        "046D",
        "pid":        "085E",
    },
    {
        "product_id": "NET-ASUS-USB-AC68",
        "name":       "ASUS USB-AC68 WiFi Adapter",
        "vendor":     "ASUSTeK",
        "type":       "Network",
        "vid":        "0B05",
        "pid":        "17F8",
    },
    {
        "product_id": "MCU-RASPBERRY-PICO",
        "name":       "Raspberry Pi Pico",
        "vendor":     "Raspberry Pi Foundation",
        "type":       "Microcontroller",
        "vid":        "2E8A",
        "pid":        "0005",
    },
]

_USB_PORTS = ["USB 3.0 Port 1", "USB 3.0 Port 2", "USB 2.0 Port 1",
              "USB 2.0 Port 2", "USB-C Port 1", "USB-C Port 2",
              "USB Hub Port 3", "USB Hub Port 4"]


# ── Firmware version database ────────────────────────────────────────────

_FIRMWARE_DB = {
    "MCU-STM32F4": [
        {"version": "3.2.1", "release_date": "2026-03-15", "size": "284 KB",
         "latest": True,  "stable": True,
         "notes": "• Fixed USB enumeration race condition on fast hosts\n"
                  "• Improved ADC calibration accuracy (+12 %)\n"
                  "• Reduced idle power consumption by 8 mW\n"
                  "• Security patch: CVE-2026-1042 (buffer overread in DFU handler)"},
        {"version": "3.1.0", "release_date": "2025-11-20", "size": "281 KB",
         "latest": False, "stable": True,
         "notes": "• Added USB CDC virtual-COM port support\n"
                  "• HAL timer improvements for better PWM resolution\n"
                  "• Bug fixes in SPI DMA transfers"},
        {"version": "2.9.4", "release_date": "2025-07-08", "size": "265 KB",
         "latest": False, "stable": False,
         "notes": "• Legacy release — upgrade recommended\n"
                  "• Known issue: occasional USB disconnect under high load"},
    ],
    "MCU-ARDUINO-MEGA": [
        {"version": "1.8.6", "release_date": "2026-01-30", "size": "48 KB",
         "latest": True,  "stable": True,
         "notes": "• Bootloader hardened against glitch attacks\n"
                  "• UART speed now stable at 2 Mbaud\n"
                  "• Fixed EEPROM wear-levelling bug"},
        {"version": "1.7.2", "release_date": "2025-09-10", "size": "46 KB",
         "latest": False, "stable": True,
         "notes": "• Improved USB-HID descriptor compliance\n"
                  "• Minor timing fixes for I2C at 400 kHz"},
    ],
    "AUDIO-FOCUSRITE-2I2": [
        {"version": "4.6.0", "release_date": "2026-02-28", "size": "1.2 MB",
         "latest": True,  "stable": True,
         "notes": "• 192 kHz sample-rate support added\n"
                  "• Latency reduced to <2 ms at 64-sample buffer\n"
                  "• Fixes for macOS 15 Sequoia driver compatibility\n"
                  "• Improved gain-step linearity on Mic preamps"},
        {"version": "4.4.1", "release_date": "2025-08-15", "size": "1.1 MB",
         "latest": False, "stable": True,
         "notes": "• Windows 11 24H2 driver fixes\n"
                  "• MIDI clock jitter improvements"},
        {"version": "4.2.0", "release_date": "2025-03-01", "size": "1.0 MB",
         "latest": False, "stable": False,
         "notes": "• Legacy release — upgrade to 4.6.0 recommended"},
    ],
    "STORAGE-SANDISK-EXTREME": [
        {"version": "2.3.4", "release_date": "2026-04-01", "size": "320 KB",
         "latest": True,  "stable": True,
         "notes": "• NVMe controller thermal throttle thresholds tuned\n"
                  "• Sequential write speed improved +7 % on large files\n"
                  "• Wear-levelling algorithm v2 deployed"},
        {"version": "2.2.0", "release_date": "2025-12-05", "size": "318 KB",
         "latest": False, "stable": True,
         "notes": "• Power-loss protection hardened\n"
                  "• SMART attribute reporting improved"},
    ],
    "INPUT-CORSAIR-K95": [
        {"version": "5.0.2", "release_date": "2026-03-20", "size": "96 KB",
         "latest": True,  "stable": True,
         "notes": "• iCUE 5 protocol support\n"
                  "• Per-key lighting sync latency reduced\n"
                  "• Fixed macro replay timing drift at high speeds"},
        {"version": "4.9.1", "release_date": "2025-10-14", "size": "94 KB",
         "latest": False, "stable": True,
         "notes": "• On-board profile storage expanded to 50 profiles\n"
                  "• G-key programmability improvements"},
        {"version": "4.7.0", "release_date": "2025-05-22", "size": "90 KB",
         "latest": False, "stable": False,
         "notes": "• End-of-support release — migrate to 5.x series"},
    ],
    "CAM-LOGITECH-BRIO": [
        {"version": "2.10.0", "release_date": "2026-02-10", "size": "2.4 MB",
         "latest": True,  "stable": True,
         "notes": "• HDR pipeline improvements for backlit scenes\n"
                  "• Windows Hello IR calibration update\n"
                  "• Auto-focus speed increased by 30 %\n"
                  "• Fixed 4K 60 fps USB bandwidth negotiation bug"},
        {"version": "2.8.3", "release_date": "2025-07-30", "size": "2.2 MB",
         "latest": False, "stable": True,
         "notes": "• Privacy shutter LED behavior corrected\n"
                  "• UVC 1.5 descriptor compliance fixes"},
    ],
    "NET-ASUS-USB-AC68": [
        {"version": "3.0.7", "release_date": "2026-01-12", "size": "512 KB",
         "latest": True,  "stable": True,
         "notes": "• WPA3-Enterprise support added\n"
                  "• Improved 5 GHz DFS channel recovery time\n"
                  "• MU-MIMO scheduling algorithm tuned"},
        {"version": "2.9.5", "release_date": "2025-09-01", "size": "508 KB",
         "latest": False, "stable": True,
         "notes": "• Security patch: PMF enforcement hardened\n"
                  "• Beacon interval accuracy improved"},
    ],
    "MCU-RASPBERRY-PICO": [
        {"version": "1.5.1", "release_date": "2026-03-05", "size": "64 KB",
         "latest": True,  "stable": True,
         "notes": "• MicroPython 1.24 bundled\n"
                  "• PIO state machine improvements\n"
                  "• USB MIDI class driver added\n"
                  "• Flash XIP performance +15 %"},
        {"version": "1.4.0", "release_date": "2025-11-10", "size": "61 KB",
         "latest": False, "stable": True,
         "notes": "• SDK 2.1 compatibility\n"
                  "• Watchdog timer reliability fix"},
        {"version": "1.2.3", "release_date": "2025-06-20", "size": "58 KB",
         "latest": False, "stable": False,
         "notes": "• Legacy release — upgrade to 1.5.x recommended"},
    ],
}

# Firmware versions that are "currently installed" on mock devices
_CURRENT_FW = {
    "MCU-STM32F4":            "3.1.0",
    "MCU-ARDUINO-MEGA":       "1.7.2",
    "AUDIO-FOCUSRITE-2I2":    "4.4.1",
    "STORAGE-SANDISK-EXTREME":"2.3.4",   # already latest
    "INPUT-CORSAIR-K95":      "4.7.0",
    "CAM-LOGITECH-BRIO":      "2.8.3",
    "NET-ASUS-USB-AC68":      "2.9.5",
    "MCU-RASPBERRY-PICO":     "1.2.3",
}


# ── Public API ────────────────────────────────────────────────────────────

class MockUSBDeviceScanner:
    """Simulates USB bus scanning — returns a random subset of known devices."""

    def scan(self) -> list:
        # Randomly connect 4-7 devices to simulate real variability
        count   = random.randint(4, len(_DEVICE_CATALOGUE))
        picked  = random.sample(_DEVICE_CATALOGUE, count)
        devices = []
        ports   = random.sample(_USB_PORTS, len(picked))

        for dev, port in zip(picked, ports):
            devices.append({
                **dev,
                "current_fw": _CURRENT_FW[dev["product_id"]],
                "port":       port,
            })
        return devices


class MockFirmwareRepository:
    """Returns available firmware versions for a given product ID."""

    def get_versions(self, product_id: str) -> list:
        return _FIRMWARE_DB.get(product_id, [])
