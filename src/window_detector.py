"""
MÃ³dulo para detectar ventanas abiertas actualmente en Windows.
Detecta apps realmente visibles/activas, no solo procesos en background.
"""

import pygetwindow as gw
from src.config import BLOCKED_APPS

def get_open_windows():
    """
    Obtiene todas las ventanas abiertas actualmente.
    Retorna una lista de tuplas (tÃ­tulo, nombre_proceso)
    """
    windows = []
    try:
        all_windows = gw.getAllWindows()
        for window in all_windows:
            # Filtrar ventanas sin tÃ­tulo o minimizadas
            if window.title and not window.isMinimized:
                windows.append({
                    'title': window.title,
                    'isActive': window.isActive
                })
    except Exception as e:
        print(f"[Error] No se pudieron obtener las ventanas: {e}")
    
    return windows

def find_blocked_apps():
    """
    Busca apps bloqueadas entre las ventanas abiertas.
    Retorna lista de apps bloqueadas que estÃ¡n abiertas.
    """
    open_windows = get_open_windows()
    blocked_found = []
    
    for window in open_windows:
        window_title = window['title'].lower()
        
        for app in BLOCKED_APPS:
            app_name = app.lower().replace('.exe', '')
            
            # Buscar coincidencia en el tÃ­tulo de la ventana
            if app_name in window_title or app.lower() in window_title:
                if window_title not in [b['title'].lower() for b in blocked_found]:
                    blocked_found.append({
                        'title': window['title'],
                        'app': app,
                        'isActive': window['isActive']
                    })
    
    return blocked_found

def get_active_window():
    """
    Obtiene la ventana actualmente activa/en foco.
    Retorna el tÃ­tulo de la ventana o None.
    """
    try:
        active = gw.getActiveWindow()
        if active:
            return active.title
    except Exception as e:
        print(f"[Error] No se pudo obtener la ventana activa: {e}")
    
    return None

def is_blocked_app_active():
    """
    Verifica si una app bloqueada estÃ¡ actualmente activa (en foco).
    Retorna el nombre de la app bloqueada o None.
    """
    active_window = get_active_window()
    if not active_window:
        return None
    
    active_lower = active_window.lower()
    
    for app in BLOCKED_APPS:
        app_name = app.lower().replace('.exe', '')
        if app_name in active_lower or app.lower() in active_lower:
            return app
    
    return None

