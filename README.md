# ⚡ USB Firmware Manager

A cross-platform desktop application for scanning, managing, and upgrading firmware on USB-connected devices — built with **Python 3** and **PyQt5**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Workflow Walkthrough](#-workflow-walkthrough)
- [Configuration](#-configuration)
- [Running Tests](#-running-tests)
- [Production Roadmap](#-production-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **USB Device Scanning** | Detects all connected USB devices with vendor, VID/PID, and port info |
| 📋 **Device Details** | Displays current firmware version, device type, and connection port |
| 🗂️ **Firmware Catalogue** | Lists available firmware versions (latest, stable, legacy) per device |
| 📝 **Release Notes** | Shows full release notes for every firmware version |
| ⬆️ **Firmware Upgrade** | Step-by-step simulated flash with live progress and status messages |
| 🪵 **Activity Log** | Timestamped log of every action for audit and debugging |
| 🎨 **Dark UI** | Industrial dark theme optimised for low-light embedded dev environments |

---

## 🏛 Architecture

The application is divided into three clean, decoupled layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  FirmwareManagerWindow  ·  DeviceCard  ·  FirmwareCard      │
│              (main.py  +  styles.py)                        │
└──────────────────────────┬──────────────────────────────────┘
                  PyQt5 Signals / Slots
┌──────────────────────────▼──────────────────────────────────┐
│                  APPLICATION LOGIC LAYER                    │
│         ScanWorker (QThread)  ·  FirmwareUpdateWorker       │
│                        (main.py)                            │
└──────────────────────────┬──────────────────────────────────┘
                    Python function calls
┌──────────────────────────▼──────────────────────────────────┐
│                       DATA LAYER                            │
│   MockUSBDeviceScanner  ·  MockFirmwareRepository           │
│                      (mock_data.py)                         │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**Presentation Layer** (`main.py`, `styles.py`)
- All PyQt5 widgets and layout code
- `FirmwareManagerWindow` — main window and UI controller
- `DeviceCard` / `FirmwareCard` — rich list items that carry full data dicts
- `styles.py` — Qt stylesheet string (dark industrial theme)

**Application Logic Layer** (`main.py`)
- `ScanWorker(QThread)` — runs USB scan in a background thread; emits `progress(int)` and `result(list)` signals
- `FirmwareUpdateWorker(QThread)` — simulates firmware flash step-by-step; emits `step(str, int)` and `finished(bool, str)` signals
- Both workers communicate with the UI exclusively through Qt signals — **no direct widget access from threads**

**Data Layer** (`mock_data.py`)
- `MockUSBDeviceScanner.scan()` — returns a randomised subset of 8 realistic device profiles
- `MockFirmwareRepository.get_versions(product_id)` — returns versioned firmware entries with release notes
- In production, swap these two classes for `pyusb` + a CDN/S3 manifest client (see [Production Roadmap](#-production-roadmap))

---

## 📁 Project Structure

```
usb-firmware-manager/
│
├── main.py            # Application entry point, UI, worker threads
├── mock_data.py       # Mock USB scanner + firmware version repository
├── styles.py          # Qt stylesheet (dark industrial theme)
├── requirements.txt   # Python dependencies
├── .gitignore         # Git exclusions
└── README.md          # This file
```

---

## 🔧 Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8 + | [python.org](https://www.python.org/downloads/) |
| pip | 21 + | Bundled with Python |
| PyQt5 | 5.15 + | Installed via pip |
| OS | Windows 10/11, macOS 11+, Ubuntu 20.04+ | Any desktop OS with display server |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/usb-firmware-manager.git
cd usb-firmware-manager
```

### 2. Create and activate a virtual environment (recommended)

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python main.py
```

The application window opens immediately. No hardware devices are required — all USB data is simulated via `mock_data.py`.

---

## 🔄 Workflow Walkthrough

### Workflow 1 — Scanning for USB Devices

```
User clicks "🔍 Scan Devices"
        │
        ▼
ScanWorker (QThread) starts
        │
        ├─ Emits progress(0..100) → scan progress bar fills
        │
        ├─ MockUSBDeviceScanner.scan() runs
        │     └─ Returns 4–7 random devices from catalogue
        │
        └─ Emits result(devices) → DeviceCard items populate left pane
```

**UI changes during scan:**
- Progress bar (4 px, teal) appears below the header and fills across ~1.2 s
- Scan button is disabled and relabelled "Scanning…"
- After completion, device count label updates and button re-enables

---

### Workflow 2 — Selecting a Device

```
User clicks a device in the left pane
        │
        ▼
_on_device_selected() fires
        │
        ├─ Reads DeviceCard.device dict
        │
        ├─ Updates info card (name, vendor, VID:PID, port, current FW)
        │
        └─ MockFirmwareRepository.get_versions(product_id)
               └─ Populates firmware list (right pane)
                       ├─ ★ LATEST  (teal text)
                       ├─ ▲ STABLE  (blue text)
                       └─   LEGACY  (default text)
```

---

### Workflow 3 — Selecting a Firmware Version

```
User clicks a firmware version in the right pane
        │
        ▼
_on_fw_selected() fires
        │
        ├─ Reads FirmwareCard.firmware dict
        │
        ├─ Populates release notes text box
        │
        └─ Compares fw.version vs device.current_fw
               ├─ Same version  → Upgrade button disabled ("✅ Already on this version")
               └─ Different     → Upgrade button enabled  ("⬆ Upgrade Firmware")
```

---

### Workflow 4 — Upgrading Firmware

```
User clicks "⬆ Upgrade Firmware"
        │
        ▼
FirmwareUpdateWorker (QThread) starts
        │
        ├─ Step: "Verifying device connection…"      → progress 10 %
        ├─ Step: "Downloading firmware package…"     → progress 25 %
        ├─ Step: "Validating checksum (SHA-256)…"    → progress 40 %
        ├─ Step: "Entering bootloader mode…"         → progress 55 %
        ├─ Step: "Erasing flash memory…"             → progress 65 %
        ├─ Step: "Writing firmware blocks…"          → progress 80 %
        ├─ Step: "Verifying written data…"           → progress 90 %
        └─ Step: "Rebooting device…"                 → progress 100 %
               │
               ├─ SUCCESS (95 % probability)
               │     └─ device.current_fw updated in memory
               │        Info card refreshes
               │        Upgrade button → "✅ Already on this version"
               │
               └─ FAILURE (5 % probability)
                     └─ Error message in activity log + status bar
                        Upgrade button → "⬆ Retry Upgrade"
```

**UI changes during upgrade:**
- Upgrade button and Scan button are both disabled (prevents concurrent operations)
- Progress bar (18 px, teal→blue gradient) appears with percentage
- Each step message updates the status label in real time
- Every step is time-stamped and appended to the activity log

---

### Workflow 5 — Activity Log

The log panel at the bottom records every significant event:

| Event | Log entry example |
|---|---|
| App start | `Application started. Click Scan Devices…` |
| Scan initiated | `Initiating USB bus scan…` |
| Scan complete | `Scan complete — 6 USB device(s) found.` |
| Device selected | `Selected device: STM32F4 Discovery Board (VID 0483, PID 374B)` |
| Firmware loaded | `Loaded 3 firmware version(s) for STM32F4 Discovery Board.` |
| Flash step | `[ 40%] Validating checksum (SHA-256)…` |
| Flash success | `✅ STM32F4 Discovery Board successfully updated to firmware v3.2.1.` |
| Flash failure | `❌ Update failed for STM32F4 Discovery Board. Please reconnect…` |

---

## ⚙️ Configuration

All mock device profiles and firmware versions are defined in `mock_data.py`.

### Adding a new device

Add an entry to `_DEVICE_CATALOGUE` in `mock_data.py`:

```python
{
    "product_id": "MY-DEVICE-001",
    "name":       "My Custom Board",
    "vendor":     "Acme Corp",
    "type":       "Microcontroller",   # or Audio / Storage / Input / Camera / Network
    "vid":        "ABCD",
    "pid":        "1234",
},
```

Then add its firmware versions to `_FIRMWARE_DB`:

```python
"MY-DEVICE-001": [
    {
        "version":      "1.0.0",
        "release_date": "2026-04-10",
        "size":         "128 KB",
        "latest":       True,
        "stable":       True,
        "notes":        "Initial release.",
    },
],
```

And set its currently-installed version in `_CURRENT_FW`:

```python
"MY-DEVICE-001": "1.0.0",
```

---

## 🧪 Running Tests

Unit tests cover the data layer (scanner + repository) and core update logic.

```bash
pip install pytest
pytest tests/ -v
```

> **Note:** The `tests/` directory is a recommended addition. A starter test for `mock_data.py`:

```python
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
```

---

## 🚀 Production Roadmap

| Component | Current (Mock) | Production Replacement |
|---|---|---|
| USB enumeration | `MockUSBDeviceScanner` | `pyusb` + `libusb` via `usb.core.find(find_all=True)` |
| Firmware manifest | `MockFirmwareRepository` | HTTP GET to a versioned JSON manifest on S3 / CDN |
| Actual flashing | `time.sleep()` simulation | `dfu-util` subprocess, `pydfu`, or vendor SDK |
| Checksum validation | Logged step only | SHA-256 + RSA signature verification before flash |
| Authentication | None | OAuth2 / API key for manifest CDN access |
| Audit trail | In-app text box | `logging` module → rotating file → SIEM ingestion |
| Packaging | `python main.py` | `PyInstaller` or `cx_Freeze` → single executable |
| Auto-update | None | Background manifest polling + update notification |
| Error reporting | Status bar | Sentry / Rollbar integration |

### Production USB Enumeration (Drop-in Replacement)

```python
# Replace MockUSBDeviceScanner with this in production:
import usb.core, usb.util

class USBDeviceScanner:
    def scan(self) -> list:
        devices = []
        for dev in usb.core.find(find_all=True):
            try:
                manufacturer = usb.util.get_string(dev, dev.iManufacturer) or "Unknown"
                product      = usb.util.get_string(dev, dev.iProduct)      or "Unknown"
            except Exception:
                manufacturer, product = "Unknown", "Unknown"
            devices.append({
                "name":       product,
                "vendor":     manufacturer,
                "vid":        f"{dev.idVendor:04X}",
                "pid":        f"{dev.idProduct:04X}",
                "product_id": f"{dev.idVendor:04X}:{dev.idProduct:04X}",
                "current_fw": "unknown",
                "port":       str(dev.bus),
                "type":       "USB Device",
            })
        return devices
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

*Built with Python + PyQt5 · Designed for embedded and IoT firmware management workflows*