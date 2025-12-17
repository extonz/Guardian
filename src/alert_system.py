"""
Sistema de alertas y notificaciones avanzadas.
Múltiples sonidos, volumes, notificaciones en pantalla.
"""

import os
from playsound import playsound
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
            # Nota: playsound no soporta volumen nativo, usar osmixvolume sería lo ideal
            threading.Thread(target=playsound, args=(sound_file,), daemon=True).start()
        except Exception as e:
            print(f"Error reproduciendo alerta: {e}")

def show_toast_notification(title, message, duration=3000):
    """Muestra notificación tipo Windows Toast (Windows 10+)."""
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=duration, threaded=True)
    except ImportError:
        # Fallback: mostrar en consola
        print(f"\n🔔 [{title}] {message}")
    except Exception as e:
        print(f"Error mostrando notificación: {e}")

def show_system_alert(title, message):
    """Muestra alerta del sistema (MessageBox)."""
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x30)
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
