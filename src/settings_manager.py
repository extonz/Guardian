"""
Gestor de configuraciÃ³n y persistencia de datos.
Guarda/carga settings, listas de apps, estadÃ­sticas, etc.
"""

import json
import os
from datetime import datetime
from src.config import BLOCKED_APPS

SETTINGS_FILE = "guardian_settings.json"
STATS_FILE = "guardian_stats.json"

DEFAULT_SETTINGS = {
    "blocked_apps": BLOCKED_APPS,
    "whitelist_apps": [],
    "password": "",
    "alert_sound": "alerta.mp3",
    "alert_volume": 100,
    "countdown_seconds": 3,
    "check_interval": 5,
    "enabled": True,
    "current_profile": "default",
    "profiles": {
        "default": {
            "name": "Por Defecto",
            "blocked_apps": BLOCKED_APPS,
            "enabled_hours": {"start": 0, "end": 24},  # 0-24 = todo el dÃ­a
        },
        "estudio": {
            "name": "Modo Estudio",
            "blocked_apps": BLOCKED_APPS,
            "enabled_hours": {"start": 8, "end": 18},
        },
        "trabajo": {
            "name": "Modo Trabajo",
            "blocked_apps": BLOCKED_APPS,
            "enabled_hours": {"start": 9, "end": 17},
        }
    }
}

def load_settings():
    """Carga los settings del archivo. Si no existe, crea uno nuevo."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] No se pudo cargar settings: {e}")
            return DEFAULT_SETTINGS
    else:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Guarda los settings en archivo."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Error] No se pudo guardar settings: {e}")
        return False

def get_blocked_apps():
    """Obtiene lista de apps bloqueadas actual."""
    settings = load_settings()
    profile = settings['current_profile']
    return settings['profiles'][profile]['blocked_apps']

def add_blocked_app(app_name):
    """Agrega una app a la lista de bloqueadas."""
    settings = load_settings()
    profile = settings['current_profile']
    if app_name not in settings['profiles'][profile]['blocked_apps']:
        settings['profiles'][profile]['blocked_apps'].append(app_name)
        save_settings(settings)
        return True
    return False

def remove_blocked_app(app_name):
    """Elimina una app de la lista de bloqueadas."""
    settings = load_settings()
    profile = settings['current_profile']
    if app_name in settings['profiles'][profile]['blocked_apps']:
        settings['profiles'][profile]['blocked_apps'].remove(app_name)
        save_settings(settings)
        return True
    return False

def add_to_whitelist(app_name):
    """Agrega una app a la whitelist."""
    settings = load_settings()
    if app_name not in settings['whitelist_apps']:
        settings['whitelist_apps'].append(app_name)
        save_settings(settings)
        return True
    return False

def remove_from_whitelist(app_name):
    """Elimina una app de la whitelist."""
    settings = load_settings()
    if app_name in settings['whitelist_apps']:
        settings['whitelist_apps'].remove(app_name)
        save_settings(settings)
        return True
    return False

def get_whitelist():
    """Obtiene la whitelist."""
    settings = load_settings()
    return settings['whitelist_apps']

def set_password(password):
    """Guarda una contraseÃ±a para proteger Guardian."""
    settings = load_settings()
    settings['password'] = password
    save_settings(settings)

def verify_password(password):
    """Verifica si la contraseÃ±a es correcta."""
    settings = load_settings()
    return settings['password'] == password

def log_block_event(app_name, timestamp=None):
    """Registra un evento de bloqueo en las estadÃ­sticas."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    stats = load_stats()
    if 'blocks' not in stats:
        stats['blocks'] = []
    
    stats['blocks'].append({
        'app': app_name,
        'timestamp': timestamp
    })
    
    save_stats(stats)

def load_stats():
    """Carga las estadÃ­sticas."""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Error] No se pudo cargar stats: {e}")
            return {"blocks": []}
    return {"blocks": []}

def save_stats(stats):
    """Guarda las estadÃ­sticas."""
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Error] No se pudo guardar stats: {e}")
        return False

def get_session_stats():
    """Retorna estadÃ­sticas de la sesiÃ³n actual."""
    stats = load_stats()
    blocks = stats.get('blocks', [])
    
    # Contar bloques de hoy
    today = datetime.now().strftime("%Y-%m-%d")
    today_blocks = [b for b in blocks if b['timestamp'].startswith(today)]
    
    # Apps mÃ¡s bloqueadas
    app_counts = {}
    for block in today_blocks:
        app = block['app']
        app_counts[app] = app_counts.get(app, 0) + 1
    
    return {
        'total_blocks_today': len(today_blocks),
        'apps_blocked': app_counts,
        'most_blocked': max(app_counts, key=app_counts.get) if app_counts else None,
    }

def switch_profile(profile_name):
    """Cambia el perfil activo."""
    settings = load_settings()
    if profile_name in settings['profiles']:
        settings['current_profile'] = profile_name
        save_settings(settings)
        return True
    return False

def get_current_profile():
    """Obtiene el perfil actual."""
    settings = load_settings()
    return settings['current_profile']

def get_profiles():
    """Obtiene todos los perfiles."""
    settings = load_settings()
    return settings['profiles']

