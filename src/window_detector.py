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
    """
    Emit a one-time warning that window monitoring is disabled because `pygetwindow` is unavailable.
    
    This function prints a single warning message the first time it is called; subsequent calls do nothing.
    """
    global _warned_unavailable
    if not _warned_unavailable:
        print("[Guardian] Aviso: 'pygetwindow' no está disponible. El monitoreo de ventanas quedará deshabilitado.")
        _warned_unavailable = True


def get_open_windows():
    """
    Return the list of currently open, visible windows.
    
    Each item is a dictionary with keys "title" (the window's title) and "isActive" (a boolean indicating whether the window is active).
    
    Returns:
        list[dict]: A list of window dictionaries; returns an empty list if window enumeration is unavailable or an error occurs.
    """
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
    """
    Find blocked applications among currently open windows.
    
    Scans visible open window titles and matches them against configured BLOCKED_APPS (case-insensitive, ".exe" suffix ignored) to identify any running blocked applications. Each matched window is returned once (duplicate titles are deduplicated regardless of case).
    
    Returns:
        list[dict]: A list of matches where each dict contains:
            - "title" (str): the window's title as reported by the system.
            - "app" (str): the blocked app entry from BLOCKED_APPS that matched.
            - "isActive" (bool): whether the matched window is currently active.
    """
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
    """
    Retrieve the title of the currently active window.
    
    Returns:
        str or None: The active window's title, or `None` if no active window is available, the pygetwindow dependency is missing, or an error occurred while retrieving it.
    """
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
    """
    Determine which blocked application, if any, corresponds to the currently active window.
    
    Matches are case-insensitive and compare the active window title against each entry in BLOCKED_APPS
    with any trailing ".exe" removed from the blocked name.
    
    Returns:
        str or None: The blocked application name from BLOCKED_APPS that matches the active window,
        or `None` if no blocked application is active or no active window is available.
    """
    active_window = get_active_window()
    if not active_window:
        return None

    active_lower = active_window.lower()

    for app in BLOCKED_APPS:
        app_name = app.lower().replace(".exe", "")
        if app_name in active_lower or app.lower() in active_lower:
            return app

    return None