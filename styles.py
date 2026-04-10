"""
styles.py
Dark-industrial aesthetic: deep charcoal backgrounds, amber/teal accents,
monospace typography — optimised for a firmware/embedded tooling context.
"""

APP_STYLESHEET = """
/* ── Base ─────────────────────────────────────────────────── */
QMainWindow, QWidget {
    background-color: #121418;
    color: #c8cdd8;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}

/* ── Header ──────────────────────────────────────────────── */
QFrame#header {
    background-color: #0d0f13;
    border-bottom: 1px solid #1e2330;
}

QLabel#appTitle {
    font-size: 17px;
    font-weight: 700;
    color: #e8ecf5;
    letter-spacing: 0.5px;
}

/* ── Panes ───────────────────────────────────────────────── */
QWidget#leftPane {
    background-color: #14171e;
    border-right: 1px solid #1e2330;
}

QWidget#rightPane {
    background-color: #121418;
}

QLabel#paneLabel {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #4a5568;
    margin-bottom: 2px;
}

QLabel#countLabel {
    font-size: 11px;
    color: #4a5568;
    padding-top: 2px;
}

/* ── Info card ───────────────────────────────────────────── */
QFrame#infoCard {
    background-color: #1a1e28;
    border: 1px solid #252b3a;
    border-radius: 6px;
}

QLabel#infoName {
    font-size: 14px;
    font-weight: 700;
    color: #e2e8f0;
}

QLabel#infoDetails {
    font-size: 11px;
    color: #6b7899;
    font-family: "Consolas", "Courier New", monospace;
}

/* ── Lists ───────────────────────────────────────────────── */
QListWidget#deviceList,
QListWidget#fwList {
    background-color: #1a1e28;
    border: 1px solid #252b3a;
    border-radius: 6px;
    outline: none;
    padding: 4px;
}

QListWidget#deviceList::item,
QListWidget#fwList::item {
    color: #b0b8cc;
    padding: 8px 10px;
    border-radius: 4px;
    border: none;
    margin: 2px 0;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    line-height: 1.6;
}

QListWidget#deviceList::item:selected,
QListWidget#fwList::item:selected {
    background-color: #1e3a5f;
    color: #e2ecff;
}

QListWidget#deviceList::item:hover:!selected,
QListWidget#fwList::item:hover:!selected {
    background-color: #1e2535;
}

/* ── Release notes ───────────────────────────────────────── */
QTextEdit#releaseNotes {
    background-color: #1a1e28;
    border: 1px solid #252b3a;
    border-radius: 6px;
    color: #8896b0;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11.5px;
    padding: 8px;
}

/* ── Progress bars ───────────────────────────────────────── */
QProgressBar#scanBar {
    background-color: #0d0f13;
    border: none;
}
QProgressBar#scanBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b4d8, stop:1 #0077b6);
}

QProgressBar#updateBar {
    background-color: #1a1e28;
    border: 1px solid #252b3a;
    border-radius: 4px;
    text-align: center;
    font-size: 11px;
    color: #6b7899;
}
QProgressBar#updateBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4aa, stop:1 #0077b6);
    border-radius: 3px;
}

QLabel#updateStatus {
    font-size: 11px;
    color: #7eb8f7;
    font-family: "Consolas", monospace;
}

/* ── Buttons ─────────────────────────────────────────────── */
QPushButton#scanBtn {
    background-color: #1a3a5c;
    color: #7eb8f7;
    border: 1px solid #2a5080;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    padding: 0 12px;
}
QPushButton#scanBtn:hover  { background-color: #224472; }
QPushButton#scanBtn:pressed { background-color: #1a3a5c; }
QPushButton#scanBtn:disabled { color: #3a4a60; border-color: #1e2a3a; }

QPushButton#upgradeBtn {
    background-color: #0d3d2e;
    color: #00d4aa;
    border: 1px solid #1a6050;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.3px;
}
QPushButton#upgradeBtn:hover   { background-color: #124d3a; }
QPushButton#upgradeBtn:pressed { background-color: #0d3d2e; }
QPushButton#upgradeBtn:disabled {
    background-color: #141a20;
    color: #2e4a42;
    border-color: #1a2830;
}

QPushButton#clearBtn {
    background-color: #1e2330;
    color: #4a5568;
    border: 1px solid #252b3a;
    border-radius: 4px;
    font-size: 11px;
}
QPushButton#clearBtn:hover { background-color: #252b3a; color: #7eb8f7; }

/* ── Log panel ───────────────────────────────────────────── */
QFrame#logFrame {
    background-color: #0e1016;
    border-top: 1px solid #1e2330;
}

QTextEdit#logBox {
    background-color: #0e1016;
    border: none;
    color: #4a5a70;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 11.5px;
}

/* ── Status bar ──────────────────────────────────────────── */
QStatusBar#statusBar {
    background-color: #0a0c10;
    color: #3a4a60;
    font-size: 11px;
    border-top: 1px solid #161a24;
}

/* ── Splitter ────────────────────────────────────────────── */
QSplitter::handle {
    background-color: #1e2330;
}

/* ── Scrollbars ──────────────────────────────────────────── */
QScrollBar:vertical {
    background: #14171e;
    width: 6px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #2a3248;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #3a4860; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #14171e;
    height: 6px;
}
QScrollBar::handle:horizontal {
    background: #2a3248;
    border-radius: 3px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover { background: #3a4860; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""
