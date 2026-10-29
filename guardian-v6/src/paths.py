"""Platform-correct application data paths."""
from pathlib import Path
import os

APP_NAME = "Guardian"

def data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif os.sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path

def config_dir() -> Path:
    path = data_dir() / "config"
    path.mkdir(parents=True, exist_ok=True)
    return path
