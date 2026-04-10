import sys
import time
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QFrame,
    QProgressBar, QTextEdit, QSplitter, QStatusBar, QGroupBox,
    QAbstractItemView, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush

from mock_data import MockUSBDeviceScanner, MockFirmwareRepository
from styles import APP_STYLESHEET


# ─────────────────────────────────────────────
#  Background worker threads
# ─────────────────────────────────────────────

class ScanWorker(QThread):
    """Scans for USB devices in the background so the UI stays responsive."""
    progress = pyqtSignal(int)
    result   = pyqtSignal(list)
    finished = pyqtSignal()

    def run(self):
        scanner = MockUSBDeviceScanner()
        for i in range(0, 101, 10):
            self.progress.emit(i)
            time.sleep(0.12)
        devices = scanner.scan()
        self.result.emit(devices)
        self.finished.emit()


class FirmwareUpdateWorker(QThread):
    """Simulates a firmware flash with step-by-step progress."""
    step     = pyqtSignal(str, int)   # (message, percent)
    finished = pyqtSignal(bool, str)  # (success, message)

    def __init__(self, device, firmware):
        super().__init__()
        self.device   = device
        self.firmware = firmware

    def run(self):
        steps = [
            ("Verifying device connection…",    10),
            ("Downloading firmware package…",   25),
            ("Validating checksum (SHA-256)…",  40),
            ("Entering bootloader mode…",        55),
            ("Erasing flash memory…",            65),
            ("Writing firmware blocks…",         80),
            ("Verifying written data…",          90),
            ("Rebooting device…",               100),
        ]
        for msg, pct in steps:
            self.step.emit(msg, pct)
            time.sleep(random.uniform(0.4, 0.9))

        success = random.random() > 0.05          # 95 % success rate
        if success:
            self.finished.emit(True,
                f"✅  {self.device['name']} successfully updated to "
                f"firmware v{self.firmware['version']}.")
        else:
            self.finished.emit(False,
                f"❌  Update failed for {self.device['name']}. "
                "Please reconnect the device and retry.")


# ─────────────────────────────────────────────
#  Custom widgets
# ─────────────────────────────────────────────

class DeviceCard(QListWidgetItem):
    """A rich list item that carries the full device dict."""
    def __init__(self, device: dict):
        icon_map = {"Microcontroller": "⚡", "Audio": "🎵",
                    "Storage": "💾", "Input": "⌨️",
                    "Camera": "📷", "Network": "🌐"}
        icon = icon_map.get(device["type"], "🔌")
        label = f"{icon}  {device['name']}\n     {device['type']}  ·  fw {device['current_fw']}"
        super().__init__(label)
        self.device = device
        self.setFont(QFont("Consolas", 10))


class FirmwareCard(QListWidgetItem):
    """A list item for one firmware version."""
    def __init__(self, fw: dict):
        badge = "★ LATEST" if fw.get("latest") else ("▲ STABLE" if fw.get("stable") else "  LEGACY")
        label = f"v{fw['version']}  [{badge}]\n  Released {fw['release_date']}  ·  {fw['size']}"
        super().__init__(label)
        self.firmware = fw
        self.setFont(QFont("Consolas", 10))
        if fw.get("latest"):
            self.setForeground(QColor("#00d4aa"))
        elif fw.get("stable"):
            self.setForeground(QColor("#7eb8f7"))


# ─────────────────────────────────────────────
#  Main window
# ─────────────────────────────────────────────

class FirmwareManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ USB Firmware Manager")
        self.setMinimumSize(1100, 720)
        self.resize(1200, 780)

        self.repo       = MockFirmwareRepository()
        self.devices    = []
        self.sel_device = None
        self.sel_fw     = None

        self._build_ui()
        self.setStyleSheet(APP_STYLESHEET)
        self._log("Application started. Click  Scan Devices  to detect connected USB hardware.")

    # ── UI construction ───────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── header bar ──
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(24, 0, 24, 0)

        title = QLabel("⚡  USB Firmware Manager")
        title.setObjectName("appTitle")
        hlay.addWidget(title)
        hlay.addStretch()

        self.scan_btn = QPushButton("🔍  Scan Devices")
        self.scan_btn.setObjectName("scanBtn")
        self.scan_btn.setFixedSize(160, 36)
        self.scan_btn.clicked.connect(self._start_scan)
        hlay.addWidget(self.scan_btn)

        root.addWidget(header)

        # ── scan progress bar (hidden until scan) ──
        self.scan_bar = QProgressBar()
        self.scan_bar.setObjectName("scanBar")
        self.scan_bar.setFixedHeight(4)
        self.scan_bar.setTextVisible(False)
        self.scan_bar.hide()
        root.addWidget(self.scan_bar)

        # ── main content splitter ──
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        # left pane – device list
        left = QWidget()
        left.setObjectName("leftPane")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(16, 16, 16, 16)
        ll.setSpacing(10)

        lbl_dev = QLabel("USB DEVICES")
        lbl_dev.setObjectName("paneLabel")
        ll.addWidget(lbl_dev)

        self.device_list = QListWidget()
        self.device_list.setObjectName("deviceList")
        self.device_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.device_list.itemSelectionChanged.connect(self._on_device_selected)
        ll.addWidget(self.device_list)

        self.device_count = QLabel("No devices found yet")
        self.device_count.setObjectName("countLabel")
        ll.addWidget(self.device_count)

        splitter.addWidget(left)

        # right pane – firmware panel
        right = QWidget()
        right.setObjectName("rightPane")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(16, 16, 16, 16)
        rl.setSpacing(10)

        lbl_fw = QLabel("AVAILABLE FIRMWARE")
        lbl_fw.setObjectName("paneLabel")
        rl.addWidget(lbl_fw)

        # device info card
        self.device_info = QFrame()
        self.device_info.setObjectName("infoCard")
        info_lay = QVBoxLayout(self.device_info)
        info_lay.setContentsMargins(14, 10, 14, 10)
        self.info_name    = QLabel("— select a device —")
        self.info_name.setObjectName("infoName")
        self.info_details = QLabel("")
        self.info_details.setObjectName("infoDetails")
        info_lay.addWidget(self.info_name)
        info_lay.addWidget(self.info_details)
        rl.addWidget(self.device_info)

        self.fw_list = QListWidget()
        self.fw_list.setObjectName("fwList")
        self.fw_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.fw_list.itemSelectionChanged.connect(self._on_fw_selected)
        rl.addWidget(self.fw_list)

        # release notes
        notes_lbl = QLabel("RELEASE NOTES")
        notes_lbl.setObjectName("paneLabel")
        rl.addWidget(notes_lbl)

        self.release_notes = QTextEdit()
        self.release_notes.setObjectName("releaseNotes")
        self.release_notes.setReadOnly(True)
        self.release_notes.setFixedHeight(90)
        self.release_notes.setPlaceholderText("Select a firmware version to read release notes…")
        rl.addWidget(self.release_notes)

        # update progress
        self.update_bar = QProgressBar()
        self.update_bar.setObjectName("updateBar")
        self.update_bar.setFixedHeight(18)
        self.update_bar.setValue(0)
        self.update_bar.hide()
        rl.addWidget(self.update_bar)

        self.update_status = QLabel("")
        self.update_status.setObjectName("updateStatus")
        self.update_status.hide()
        rl.addWidget(self.update_status)

        # upgrade button
        self.upgrade_btn = QPushButton("⬆   Upgrade Firmware")
        self.upgrade_btn.setObjectName("upgradeBtn")
        self.upgrade_btn.setFixedHeight(42)
        self.upgrade_btn.setEnabled(False)
        self.upgrade_btn.clicked.connect(self._start_update)
        rl.addWidget(self.upgrade_btn)

        splitter.addWidget(right)
        splitter.setSizes([380, 720])

        root.addWidget(splitter, 1)

        # ── log panel ──
        log_frame = QFrame()
        log_frame.setObjectName("logFrame")
        log_frame.setFixedHeight(120)
        log_lay = QVBoxLayout(log_frame)
        log_lay.setContentsMargins(16, 8, 16, 8)
        log_lay.setSpacing(4)

        log_hdr = QHBoxLayout()
        log_label = QLabel("ACTIVITY LOG")
        log_label.setObjectName("paneLabel")
        log_hdr.addWidget(log_label)
        log_hdr.addStretch()
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clearBtn")
        clear_btn.setFixedSize(56, 22)
        clear_btn.clicked.connect(lambda: self.log_box.clear())
        log_hdr.addWidget(clear_btn)
        log_lay.addLayout(log_hdr)

        self.log_box = QTextEdit()
        self.log_box.setObjectName("logBox")
        self.log_box.setReadOnly(True)
        log_lay.addWidget(self.log_box)

        root.addWidget(log_frame)

        # status bar
        self.status = QStatusBar()
        self.status.setObjectName("statusBar")
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

    # ── scan logic ────────────────────────────

    def _start_scan(self):
        self.scan_btn.setEnabled(False)
        self.scan_btn.setText("Scanning…")
        self.device_list.clear()
        self.fw_list.clear()
        self.release_notes.clear()
        self.upgrade_btn.setEnabled(False)
        self.sel_device = None
        self.sel_fw     = None
        self.scan_bar.setValue(0)
        self.scan_bar.show()
        self._log("Initiating USB bus scan…")
        self.status.showMessage("Scanning USB devices…")

        self._scan_worker = ScanWorker()
        self._scan_worker.progress.connect(self.scan_bar.setValue)
        self._scan_worker.result.connect(self._on_scan_result)
        self._scan_worker.finished.connect(self._on_scan_done)
        self._scan_worker.start()

    def _on_scan_result(self, devices):
        self.devices = devices
        for d in devices:
            self.device_list.addItem(DeviceCard(d))
        self.device_count.setText(f"{len(devices)} device(s) detected")
        self._log(f"Scan complete — {len(devices)} USB device(s) found.")

    def _on_scan_done(self):
        self.scan_bar.hide()
        self.scan_btn.setEnabled(True)
        self.scan_btn.setText("🔍  Scan Devices")
        self.status.showMessage(f"Scan finished — {len(self.devices)} device(s) connected.")

    # ── device selection ──────────────────────

    def _on_device_selected(self):
        items = self.device_list.selectedItems()
        if not items:
            return
        self.sel_device = items[0].device
        d = self.sel_device
        self.info_name.setText(d["name"])
        self.info_details.setText(
            f"Vendor: {d['vendor']}   ·   VID:PID {d['vid']}:{d['pid']}   ·   "
            f"Current FW: v{d['current_fw']}   ·   Port: {d['port']}"
        )
        self._load_firmware(d)
        self._log(f"Selected device: {d['name']}  (VID {d['vid']}, PID {d['pid']})")

    def _load_firmware(self, device):
        self.fw_list.clear()
        self.release_notes.clear()
        self.upgrade_btn.setEnabled(False)
        versions = self.repo.get_versions(device["product_id"])
        for fw in versions:
            self.fw_list.addItem(FirmwareCard(fw))
        self._log(f"Loaded {len(versions)} firmware version(s) for {device['name']}.")

    # ── firmware selection ────────────────────

    def _on_fw_selected(self):
        items = self.fw_list.selectedItems()
        if not items:
            return
        self.sel_fw = items[0].firmware
        fw = self.sel_fw
        self.release_notes.setPlainText(fw.get("notes", "No release notes available."))

        cur = self.sel_device["current_fw"] if self.sel_device else ""
        can_upgrade = (fw["version"] != cur)
        self.upgrade_btn.setEnabled(can_upgrade)
        if not can_upgrade:
            self.upgrade_btn.setText("✅  Already on this version")
        else:
            self.upgrade_btn.setText("⬆   Upgrade Firmware")

    # ── firmware update ───────────────────────

    def _start_update(self):
        if not self.sel_device or not self.sel_fw:
            return
        self.upgrade_btn.setEnabled(False)
        self.scan_btn.setEnabled(False)
        self.update_bar.setValue(0)
        self.update_bar.show()
        self.update_status.setText("Preparing update…")
        self.update_status.show()
        self._log(f"Starting firmware update: {self.sel_device['name']}  →  "
                  f"v{self.sel_fw['version']}")
        self.status.showMessage("Flashing firmware — do not disconnect device…")

        self._update_worker = FirmwareUpdateWorker(self.sel_device, self.sel_fw)
        self._update_worker.step.connect(self._on_update_step)
        self._update_worker.finished.connect(self._on_update_done)
        self._update_worker.start()

    def _on_update_step(self, msg, pct):
        self.update_bar.setValue(pct)
        self.update_status.setText(msg)
        self._log(f"  [{pct:>3}%] {msg}")

    def _on_update_done(self, success, msg):
        self.update_bar.hide()
        self.update_status.hide()
        self.scan_btn.setEnabled(True)
        self._log(msg)
        self.status.showMessage(msg)

        if success:
            # update the mock device's firmware version in-place
            self.sel_device["current_fw"] = self.sel_fw["version"]
            self.info_details.setText(
                f"Vendor: {self.sel_device['vendor']}   ·   "
                f"VID:PID {self.sel_device['vid']}:{self.sel_device['pid']}   ·   "
                f"Current FW: v{self.sel_device['current_fw']}   ·   "
                f"Port: {self.sel_device['port']}"
            )
            self.upgrade_btn.setText("✅  Already on this version")
        else:
            self.upgrade_btn.setEnabled(True)
            self.upgrade_btn.setText("⬆   Retry Upgrade")

    # ── helpers ───────────────────────────────

    def _log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.log_box.append(f'<span style="color:#555;">[{ts}]</span>  {msg}')


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = FirmwareManagerWindow()
    win.show()
    sys.exit(app.exec_())
