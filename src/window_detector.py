"""
Módulo para detectar ventanas abiertas.
Si `pygetwindow` no está disponible, el detector se desactiva de forma segura.
"""

from src.config import BLOCKED_APPS

try:
    import pygetwindow as gw
except Exception:
    gw = None

_warned_unavailable = False


def _warn_unavailable_once():
    global _warned_unavailable
    if not _warned_unavailable:
        print("[Guardian] Aviso: 'pygetwindow' no está disponible. El monitoreo de ventanas quedará deshabilitado.")
        _warned_unavailable = True


def get_open_windows():
    """Obtiene ventanas abiertas visibles."""
    if gw is None:
        _warn_unavailable_once()
        return []

    windows = []
    try:
        for window in gw.getAllWindows():
            if window.title and not window.isMinimized:
                windows.append({
                    "title": window.title,
                    "isActive": window.isActive,
                })
    except Exception as e:
        print(f"[Error] No se pudieron obtener las ventanas: {e}")

    return windows


def find_blocked_apps():
    """Busca apps bloqueadas entre ventanas abiertas."""
    open_windows = get_open_windows()
    blocked_found = []

    for window in open_windows:
        window_title = window["title"].lower()

        for app in BLOCKED_APPS:
            app_name = app.lower().replace(".exe", "")
            if app_name in window_title or app.lower() in window_title:
                if window_title not in [b["title"].lower() for b in blocked_found]:
                    blocked_found.append(
                        {
                            "title": window["title"],
                            "app": app,
                            "isActive": window["isActive"],
                        }
                    )

    return blocked_found


def get_active_window():
    """Obtiene la ventana activa."""
    if gw is None:
        _warn_unavailable_once()
        return None

    try:
        active = gw.getActiveWindow()
        if active:
            return active.title
    except Exception as e:
        print(f"[Error] No se pudo obtener la ventana activa: {e}")

    return None


def is_blocked_app_active():
    """Verifica si una app bloqueada está activa."""
    active_window = get_active_window()
    if not active_window:
        return None

    active_lower = active_window.lower()

    for app in BLOCKED_APPS:
        app_name = app.lower().replace(".exe", "")
        if app_name in active_lower or app.lower() in active_lower:
            return app

    return None
