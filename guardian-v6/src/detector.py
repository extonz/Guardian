"""Best-effort active application/window detection."""
from __future__ import annotations
import sys
from typing import Optional

def active_window_title() -> Optional[str]:
    """Return active window title when supported; never crash the monitor."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            from ctypes import wintypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd: return None
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buffer = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
            return buffer.value or None
        except Exception:
            return None
    if sys.platform == "darwin":
        try:
            from AppKit import NSWorkspace
            app = NSWorkspace.sharedWorkspace().frontmostApplication()
            return app.localizedName() if app else None
        except Exception:
            return None
    # X11 only: Wayland deliberately degrades gracefully when denied.
    try:
        import subprocess
        result = subprocess.run(["xdotool", "getactivewindow", "getwindowname"], capture_output=True, text=True, timeout=1, check=False)
        return result.stdout.strip() or None if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired, Exception):
        return None

def is_blocked(title: str | None, blocked: list[str], whitelist: list[str]) -> bool:
    if not title: return False
    candidate = title.casefold()
    if any(item.casefold() in candidate for item in whitelist if item.strip()): return False
    return any(item.casefold() in candidate for item in blocked if item.strip())
