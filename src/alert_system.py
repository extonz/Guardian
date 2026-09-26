"""
Sistema de alertas y notificaciones avanzadas.
Múltiples sonidos, volumes, notificaciones en pantalla.
"""

import os
import threading
import ctypes

# Tipos de alertas disponibles
ALERT_TYPES = {
    "default": "alerta.mp3",
    "warning": "warning.mp3",
    "critical": "critical.mp3",
    "soft": "soft.mp3",
}

SOUND_VOLUMES = {
    "mute": 0,
    "low": 30,
    "medium": 60,
    "high": 100,
}

def play_alert(alert_type="default", volume=100):
    """Reproduce una alerta de sonido con volumen controlado."""
    sound_file = ALERT_TYPES.get(alert_type, ALERT_TYPES["default"])
    
    if os.path.exists(sound_file):
        try:
            import platform
            if platform.system() == 'Windows':
                import winsound
                threading.Thread(target=winsound.PlaySound, args=(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC), daemon=True).start()
            elif platform.system() == 'Darwin':
                threading.Thread(target=lambda: os.system(f"afplay {sound_file}"), daemon=True).start()
            else:
                threading.Thread(target=lambda: os.system(f"paplay {sound_file}"), daemon=True).start()
        except Exception as e:
            print(f"Error reproduciendo alerta: {e}")

def show_toast_notification(title, message, duration=3000):
    """Muestra notificación multiplataforma."""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name='Guardian',
            timeout=duration // 1000
        )
    except ImportError:
        # Fallback: mostrar en consola
        print(f"\n🔔 [{title}] {message}")
    except Exception as e:
        print(f"Error mostrando notificación: {e}")

def show_system_alert(title, message):
    """Muestra alerta del sistema (MessageBox)."""
    try:
        if os.name == 'nt':
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)
        else:
            print(f"⚠️ {title}: {message}")
    except Exception as e:
        print(f"Error mostrando alerta del sistema: {e}")

def create_alert_sounds():
    """Crea archivos de alerta de ejemplo si no existen."""
    # Los archivos reales necesitarían ser descargados desde MyInstants o similar
    # Por ahora creamos placeholders
    sounds_needed = ["alerta.mp3", "warning.mp3", "critical.mp3", "soft.mp3"]
    for sound in sounds_needed:
        if not os.path.exists(sound):
            print(f"⚠️ Falta {sound}. Descárgalo desde MyInstants y coloca en el directorio.")
