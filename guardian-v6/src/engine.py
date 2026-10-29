"""Cancellable monitoring worker; callbacks run on the worker thread."""
from __future__ import annotations
import threading, time
from datetime import datetime
from .detector import active_window_title, is_blocked
from .notifications import notify
from .storage import load, update

class Monitor:
    def __init__(self, on_event=None, interval: float = 2.0):
        self.on_event = on_event
        self.interval = max(0.5, interval)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_title = None
        self._last_notice = 0.0

    @property
    def running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def start(self) -> None:
        if self.running: return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="GuardianMonitor", daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 3.0) -> None:
        self._stop.set()
        if self._thread and self._thread is not threading.current_thread(): self._thread.join(timeout)

    def _run(self) -> None:
        while not self._stop.is_set():
            settings = load("settings")
            if not settings.get("zen_mode", False):
                title = active_window_title()
                blocked = settings.get("blocked_apps", [])
                whitelist = settings.get("whitelist", [])
                if is_blocked(title, blocked, whitelist) and title != self._last_title:
                    def record(stats):
                        stats["blocks"] = int(stats.get("blocks", 0)) + 1
                        stats.setdefault("events", []).append({"app": title, "at": datetime.now().isoformat(timespec="seconds")})
                        stats["events"] = stats["events"][-500:]
                    update("stats", record)
                    if settings.get("reminders", True) and time.monotonic() - self._last_notice > 30:
                        notify("Guardian", f"¿Quieres volver a lo que estabas haciendo? ({title})")
                        self._last_notice = time.monotonic()
                    if self.on_event:
                        try: self.on_event(title)
                        except Exception: pass
                self._last_title = title
            self._stop.wait(self.interval)
