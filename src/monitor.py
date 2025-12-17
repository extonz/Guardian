import time

from src.utils import check_blocked_apps
from src.config import CHECK_INTERVAL

ALERT_SOUND = "alerta.mp3"  # Guarda aquÃ­ el mp3 descargado desde MyInstants

def monitor_apps(ui_callback=None):
    print("Monitor de apps bloqueadas iniciado...")
    while True:
        check_blocked_apps(ALERT_SOUND, countdown=3, ui_callback=ui_callback)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_apps()

