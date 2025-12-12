import psutil
import time
try:
    from playsound import playsound
except Exception:
    playsound = None
import threading
from src.utils.config import BLOCKED_APPS, WARNING_TIME
from src.core.window_detector import find_blocked_apps, is_blocked_app_active
from src.utils.settings_manager import get_whitelist, log_block_event
from src.utils.logger import log_block, log_close, log_info

def kill_process_by_name(name):
    """Cierra procesos por nombre"""
    for p in psutil.process_iter(['name', 'pid']):
        try:
            if p.info['name'] and name.lower() in p.info['name'].lower():
                p.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def alert_and_kill(app_name, alert_sound_path, countdown=10, ui_callback=None):
    """
    Muestra alerta sonora y temporal antes de cerrar la app.
    """
    def countdown_thread():
        for i in range(countdown, 0, -1):
            message = f"[Guardian] '{app_name}' se cerrará en {i} segundos..."
            print(message)
            if ui_callback:
                ui_callback(message)
            time.sleep(1)
        kill_process_by_name(app_name)
        final_message = f"[Guardian] '{app_name}' ha sido cerrada."
        print(final_message)
        if ui_callback:
            ui_callback(final_message)
        log_close(app_name)
        log_block_event(app_name)

    # Reproducir sonido en otro hilo para no bloquear (fallback si no hay playsound)
    log_block(app_name)
    if playsound:
        threading.Thread(target=playsound, args=(alert_sound_path,), daemon=True).start()
    else:
        try:
            import winsound
            threading.Thread(target=winsound.MessageBeep, args=(winsound.MB_ICONEXCLAMATION,), daemon=True).start()
        except Exception:
            pass
    countdown_thread()

def check_blocked_apps(alert_sound_path, countdown=3, ui_callback=None):
    """
    Revisa las apps bloqueadas ABIERTAS (ventanas visibles).
    Solo detecta apps que realmente están abiertas, no procesos en background.
    Respeta la whitelist de excepciones.
    """
    blocked_apps_open = find_blocked_apps()
    whitelist = get_whitelist()
    
    for app_info in blocked_apps_open:
        # Verificar si está en whitelist
        if any(w.lower() in app_info['title'].lower() for w in whitelist):
            continue
        
        # Verificar si la app está en foco (activa)
        if app_info['isActive']:
            alert_and_kill(app_info['app'], alert_sound_path, countdown, ui_callback)
        else:
            # Si no está en foco, mostrar advertencia
            message = f"⚠️ Aplicación bloqueada detectada (background): {app_info['title']}"
            if ui_callback:
                ui_callback(message)
            print(message)
