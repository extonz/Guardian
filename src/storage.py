"""Atomic JSON persistence with in-process synchronization."""
from __future__ import annotations
import json, os, tempfile, threading
from pathlib import Path
from typing import Any
from .paths import config_dir

_LOCK = threading.RLock()
DEFAULTS: dict[str, Any] = {
    "settings": {"blocked_apps": ["TikTok", "Instagram", "Roblox"], "whitelist": [], "zen_mode": False, "reminders": True, "daily_goal_minutes": 120},
    "stats": {"blocks": 0, "focus_minutes": 0, "sessions": 0, "events": []},
    "profiles": {"default": {"name": "Default", "blocked_apps": ["TikTok", "Instagram", "Roblox"]}},
    "whitelist": {"apps": [], "websites": []},
}

def file_for(name: str) -> Path:
    if name not in DEFAULTS:
        raise ValueError(f"Unknown data file: {name}")
    return config_dir() / f"{name}.json"

def load(name: str) -> dict[str, Any]:
    path = file_for(name)
    with _LOCK:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else dict(DEFAULTS[name])
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            return json.loads(json.dumps(DEFAULTS[name]))

def save(name: str, value: dict[str, Any]) -> None:
    path = file_for(name)
    with _LOCK:
        fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(value, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, path)
        finally:
            try: os.unlink(temp_name)
            except FileNotFoundError: pass

def update(name: str, mutator) -> dict[str, Any]:
    with _LOCK:
        value = load(name)
        mutator(value)
        save(name, value)
        return value
