"""Application stylesheet — Editorial Club theme.

Replaces V6 « Editorial / Hero ».

Rollback :
  - theme V6 conservé dans styles_editorial_v6.py
  - theme pre-V6 conservé dans styles_legacy.py
  - git checkout pre-editorial-club-theme → revient à la V6 finale
"""
from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QFontDatabase, QPainter, QRadialGradient
from PyQt6.QtWidgets import QApplication, QWidget


def _assets_dir() -> Path:
    """Resolve the assets directory both in dev mode and inside a PyInstaller bundle."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / "src" / "assets"
    return Path(__file__).resolve().parent.parent / "assets"


def _asset_url(name: str) -> str:
    """Return a forward-slashed absolute URL suitable for use inside QSS."""
    p = _assets_dir() / name
    return p.as_posix()


# ===== Palette (Editorial Club) =====

RED = "#B82838"             # bordeaux — accents, focus, primary buttons
RED_DARK = "#9d1f2e"        # hover on primary
RED_GLOW = "#B82838"        # glow color (alpha is applied at paint time)

BLACK = "#15131a"           # page background (graphite violacé)
GREY_DARK = "#0e0c12"       # sidebar, dialogs
GREY = "#1a1620"            # panels, cards, inputs
GREY_LIGHT = "#251f2c"      # hairlines, borders

TEXT = "#f3e1c8"            # champagne — replaces pure white
TEXT_DIM = "#8e8395"

ACCENT_GOOD = "#8fbf85"
ACCENT_BAD = "#bf8585"

# Border radii — sober compared to V6 (was 14 / 10 / 22).
CARD_RADIUS = 6
INPUT_RADIUS = 4
BUTTON_RADIUS = 2


# ===== Font loading =====

# Variable fonts — one file per family + italic. Qt6 supports them natively.
_FONT_FILES = (
    "Inter[opsz,wght].ttf",
    "PlayfairDisplay[wght].ttf",
    "PlayfairDisplay-Italic[wght].ttf",
    "SourceSerif4[opsz,wght].ttf",
    "SourceSerif4-Italic[opsz,wght].ttf",
    "JetBrainsMono[wght].ttf",
)


def load_fonts(_app: QApplication | None = None) -> None:
    """Register the bundled TTFs with QFontDatabase.

    Safe to call multiple times — Qt deduplicates registrations by file path.
    If a file is missing, we log a warning to stderr and continue (Qt will
    fall back to the system families declared in the QSS font-family stack).
    """
    fonts_dir = _assets_dir() / "fonts"
    for name in _FONT_FILES:
        path = fonts_dir / name
        if not path.exists():
            print(f"[styles] missing font: {path}", file=sys.stderr)
            continue
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id == -1:
            print(f"[styles] failed to register font: {path}", file=sys.stderr)


# ===== Stylesheet =====

STYLESHEET = f"""
/* Most widgets are transparent so the radial glow can shine through.
   Specific surfaces (sidebar, cards, inputs) set their own background. */
QWidget {{
    color: {TEXT};
    font-family: "Inter", "Segoe UI", "Helvetica", sans-serif;
    font-size: 11pt;
}}

QMainWindow {{
    background-color: {BLACK};
}}

/* ----- Sidebar ----- */
#sidebar {{
    background-color: {GREY_DARK};
    border-right: 1px solid {GREY_LIGHT};
}}
#sidebar QPushButton {{
    background-color: transparent;
    color: {TEXT_DIM};
    text-align: left;
    padding: 9px 14px;
    border: none;
    font-size: 11pt;
    font-family: "Inter", "Segoe UI", sans-serif;
}}
#sidebar QPushButton:hover {{
    color: {TEXT};
}}
#sidebar QPushButton:checked {{
    background-color: transparent;
    color: {TEXT};
    font-weight: 500;
}}

#sidebarLogo {{
    background-color: {GREY_DARK};
    padding: 16px;
}}
#sidebarTitle {{
    color: {TEXT};
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 19pt;
    font-weight: 600;
    padding: 14px 22px 4px 22px;
    background-color: {GREY_DARK};
    letter-spacing: 0;
}}
#sidebarSubtitle {{
    color: {TEXT_DIM};
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 9pt;
    padding: 0 22px 14px 22px;
    background-color: {GREY_DARK};
}}
#sidebarSection {{
    color: {TEXT_DIM};
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 9pt;
    font-weight: 500;
    padding: 16px 22px 4px 22px;
    background-color: {GREY_DARK};
}}

/* ----- Primary / secondary / tertiary buttons ----- */
QPushButton {{
    background-color: {RED};
    color: {TEXT};
    border: none;
    padding: 10px 22px;
    border-radius: {BUTTON_RADIUS}px;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-weight: 500;
    font-size: 10pt;
}}
QPushButton:hover {{
    background-color: {RED_DARK};
}}
QPushButton:disabled {{
    background-color: {GREY_LIGHT};
    color: {TEXT_DIM};
}}

QPushButton#secondary {{
    background-color: transparent;
    color: {RED};
    border: 1px solid {RED};
}}
QPushButton#secondary:hover {{
    background-color: {GREY};
    color: {TEXT};
}}

QPushButton#tertiary {{
    background-color: transparent;
    color: {TEXT_DIM};
    border: none;
    padding: 10px 8px;
    font-family: "Source Serif 4", "Georgia", serif;
    font-style: italic;
    font-weight: 400;
}}
QPushButton#tertiary:hover {{
    color: {TEXT};
}}

/* ----- Inputs ----- */
QLineEdit, QSpinBox, QTextEdit, QDateEdit, QPlainTextEdit, QComboBox {{
    background-color: {GREY};
    color: {TEXT};
    border: 1px solid {GREY_LIGHT};
    border-radius: {INPUT_RADIUS}px;
    padding: 8px 12px;
    min-height: 22px;
    selection-background-color: {RED};
    selection-color: {TEXT};
    font-family: "Inter", "Segoe UI", sans-serif;
}}
QLineEdit:focus, QSpinBox:focus, QTextEdit:focus, QDateEdit:focus,
QPlainTextEdit:focus, QComboBox:focus {{
    border: 1px solid {RED};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid {GREY_LIGHT};
    border-top-right-radius: {INPUT_RADIUS}px;
    border-bottom-right-radius: {INPUT_RADIUS}px;
}}
QComboBox::down-arrow {{
    image: url({_asset_url("arrow-down.svg")});
    width: 12px;
    height: 8px;
    margin-right: 6px;
}}
QComboBox QAbstractItemView {{
    background-color: {GREY_DARK};
    color: {TEXT};
    border: 1px solid {GREY_LIGHT};
    selection-background-color: {RED};
    selection-color: {TEXT};
    padding: 4px;
    outline: 0;
}}
QComboBox QAbstractItemView::item {{
    min-height: 28px;
    padding: 6px 10px;
}}

QDateEdit::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid {GREY_LIGHT};
    border-top-right-radius: {INPUT_RADIUS}px;
    border-bottom-right-radius: {INPUT_RADIUS}px;
}}
QDateEdit::down-arrow {{
    image: url({_asset_url("calendar.svg")});
    width: 16px;
    height: 16px;
    margin-right: 6px;
}}
QCalendarWidget QWidget {{
    background-color: {GREY_DARK};
    color: {TEXT};
}}
QCalendarWidget QAbstractItemView:enabled {{
    background-color: {GREY_DARK};
    color: {TEXT};
    selection-background-color: {RED};
    selection-color: {TEXT};
}}
QCalendarWidget QAbstractItemView:disabled {{
    color: {GREY_LIGHT};
}}
QCalendarWidget QToolButton {{
    background-color: transparent;
    color: {TEXT};
    border: none;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 500;
}}
QCalendarWidget QToolButton:hover {{
    background-color: {GREY_DARK};
    color: {RED};
}}
QCalendarWidget QToolButton#qt_calendar_prevmonth,
QCalendarWidget QToolButton#qt_calendar_nextmonth {{
    color: {TEXT};
    font-size: 16pt;
    qproperty-iconSize: 0px 0px;
}}
QCalendarWidget QMenu {{
    background-color: {GREY_DARK};
    color: {TEXT};
}}
QCalendarWidget QSpinBox {{
    background-color: {GREY};
    color: {TEXT};
}}
QCalendarWidget #qt_calendar_navigationbar {{
    background-color: {GREY};
}}

/* ----- Checkboxes ----- */
QCheckBox {{
    color: {TEXT};
    spacing: 8px;
    background: transparent;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid {GREY_LIGHT};
    border-radius: 3px;
    background-color: {GREY};
}}
QCheckBox::indicator:hover {{
    border-color: {RED};
}}
QCheckBox::indicator:checked {{
    background-color: {RED};
    border-color: {RED};
    image: none;
}}
QCheckBox:disabled {{
    color: {TEXT_DIM};
}}

/* ----- Typography labels (used via setObjectName) ----- */
QLabel#h1 {{
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 28pt;
    font-weight: 600;
    color: {TEXT};
    padding-bottom: 4px;
}}
QLabel#h2 {{
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 14pt;
    font-weight: 600;
    color: {TEXT};
    padding: 12px 0 6px 0;
    letter-spacing: 0;
}}
QLabel#muted {{
    color: {TEXT_DIM};
    font-family: "Source Serif 4", "Georgia", serif;
}}
QLabel#eyebrow {{
    color: {RED};
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 9pt;
    font-weight: 600;
    padding: 0 0 6px 0;
}}
QLabel#lead {{
    color: {TEXT_DIM};
    font-family: "Source Serif 4", "Georgia", serif;
    font-size: 11pt;
    padding: 4px 0 0 0;
}}
QLabel#rule {{
    background-color: {RED};
    max-height: 1px;
    min-height: 1px;
}}

/* ----- Cards ----- */
QFrame#card {{
    background-color: {GREY};
    border: 1px solid {GREY_LIGHT};
    border-radius: {CARD_RADIUS}px;
}}

/* ----- Tables ----- */
QTableWidget {{
    background-color: transparent;
    color: {TEXT};
    gridline-color: transparent;
    border: none;
    selection-background-color: {RED_DARK};
    font-family: "Source Serif 4", "Georgia", serif;
}}
QFrame#tableWrap {{
    background-color: {GREY};
    border: 1px solid {GREY_LIGHT};
    border-radius: {CARD_RADIUS}px;
}}
QTableWidget::item {{
    background-color: transparent;
    color: {TEXT};
    padding: 6px;
}}
QHeaderView::section {{
    background-color: {GREY_DARK};
    color: {TEXT_DIM};
    padding: 8px;
    border: none;
    border-bottom: 1px solid {GREY_LIGHT};
    font-family: "Inter", "Segoe UI", sans-serif;
    font-weight: 500;
    font-size: 9pt;
    letter-spacing: 1px;
}}
QHeaderView::section:first {{
    border-top-left-radius: {CARD_RADIUS}px;
}}
QHeaderView::section:last {{
    border-top-right-radius: {CARD_RADIUS}px;
}}
QTableCornerButton::section {{
    background-color: {GREY_DARK};
    border: none;
    border-top-left-radius: {CARD_RADIUS}px;
}}

/* ----- Containers must stay transparent for the glow ----- */
QStackedWidget {{
    background-color: transparent;
}}
QScrollArea {{
    border: none;
    background-color: transparent;
}}
QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background-color: {GREY_LIGHT};
    border-radius: 5px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {RED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* ----- Dialogs ----- */
QDialog {{
    background-color: {GREY_DARK};
}}
QMessageBox {{
    background-color: {GREY_DARK};
}}
QMessageBox QLabel,
QDialog QLabel {{
    color: {TEXT};
}}

/* ----- Match card ----- */
QFrame#matchCard {{
    background-color: {GREY};
    border: 1px solid {GREY_LIGHT};
    border-radius: {CARD_RADIUS}px;
}}
QFrame#matchCard[played="true"] {{
    /* Played state is communicated by the table-pill opacity (set in code),
       not by a green left border anymore. */
}}
"""


# ===== Glow background widget =====

class GlowBackground(QWidget):
    """Page background with a subtle bordeaux radial glow in the bottom-left.

    Use as the central widget of QMainWindow (or wrap your content in it) to
    get the editorial backdrop. Other widgets are painted on top with their
    own styled backgrounds.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        bg: str = BLACK,
        glow_color: str = RED_GLOW,
        corner: str = "bottom-left",
        intensity: int = 80,
    ):
        super().__init__(parent)
        self._bg = QColor(bg)
        self._glow = QColor(glow_color)
        self._corner = corner
        self._intensity = intensity
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), self._bg)
        w, h = self.width(), self.height()
        if self._corner == "top-right":
            center = QPointF(w * 0.78, h * 0.18)
        elif self._corner == "top-left":
            center = QPointF(w * 0.20, h * 0.18)
        elif self._corner == "bottom-left":
            center = QPointF(w * 0.18, h * 0.82)
        elif self._corner == "bottom-right":
            center = QPointF(w * 0.82, h * 0.82)
        else:
            center = QPointF(w * 0.5, h * 0.5)
        radius = max(w, h) * 0.55
        g = QRadialGradient(center, radius)
        c0 = QColor(self._glow)
        c0.setAlpha(self._intensity)
        g.setColorAt(0.0, c0)
        c_mid = QColor(self._glow)
        c_mid.setAlpha(25)
        g.setColorAt(0.5, c_mid)
        end = QColor(0, 0, 0, 0)
        g.setColorAt(1.0, end)
        p.fillRect(self.rect(), g)
        p.end()
