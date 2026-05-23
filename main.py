"""Top12 — Application de gestion de tournoi de tennis de table."""
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.database import Database
from src.ui.main_window import MainWindow


def _assets_dir() -> Path:
    """Resolve the assets directory both in dev mode and inside a PyInstaller bundle."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / "src" / "assets"
    return Path(__file__).resolve().parent / "src" / "assets"


def _apply_windows_taskbar_icon():
    """On Windows the taskbar groups apps by AppUserModelID — set ours explicitly
    so the .exe shows our icon instead of being grouped under the generic Python
    interpreter."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("club.top12.app")
    except Exception:
        pass  # not fatal — icon may just fall back to the default group


def main():
    _apply_windows_taskbar_icon()

    app = QApplication(sys.argv)
    app.setApplicationName("Top12")

    assets = _assets_dir()
    icon_path = assets / "icon.ico"
    if not icon_path.exists():
        icon_path = assets / "logo.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    data_dir = Path.home() / ".top12"
    data_dir.mkdir(exist_ok=True)
    db = Database(data_dir / "top12.db")

    window = MainWindow(db)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
