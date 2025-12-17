"""
Sistema de horarios de bloqueo.
Permite horarios especÃ­ficos para cada dÃ­a y perfil.
"""

from datetime import datetime, time
from src.settings_manager import load_settings, save_settings

def is_blocking_active():
    """Verifica si el bloqueo debe estar activo segÃºn el horario."""
    settings = load_settings()
    profile = settings['current_profile']
    
    hours_config = settings['profiles'][profile].get('enabled_hours', {})
    start_hour = hours_config.get('start', 0)
    end_hour = hours_config.get('end', 24)
    
    current_hour = datetime.now().hour
    
    return start_hour <= current_hour < end_hour

def set_schedule(profile, day, start_hour, end_hour):
    """
    Configura horario de bloqueo para un dÃ­a especÃ­fico.
    day: "monday", "tuesday", ... "sunday"
    """
    settings = load_settings()
    
    if 'schedules' not in settings:
        settings['schedules'] = {}
    
    if profile not in settings['schedules']:
        settings['schedules'][profile] = {}
    
    settings['schedules'][profile][day] = {
        'start': start_hour,
        'end': end_hour,
        'enabled': True
    }
    
    save_settings(settings)
    return True

def get_todays_schedule(profile):
    """Obtiene el horario de hoy para un perfil."""
    settings = load_settings()
    
    if 'schedules' not in settings or profile not in settings['schedules']:
        return None
    
    day_name = datetime.now().strftime("%A").lower()
    return settings['schedules'][profile].get(day_name, None)

def get_all_schedules(profile):
    """Obtiene todos los horarios de un perfil."""
    settings = load_settings()
    
    if 'schedules' not in settings or profile not in settings['schedules']:
        return {}
    
    return settings['schedules'][profile]

def set_time_limit(app_name, minutes_per_day):
    """
    Permite usar una app X minutos por dÃ­a.
    DespuÃ©s cierra automÃ¡ticamente.
    """
    settings = load_settings()
    
    if 'time_limits' not in settings:
        settings['time_limits'] = {}
    
    settings['time_limits'][app_name] = {
        'minutes': minutes_per_day,
        'used': 0,
        'last_reset': datetime.now().isoformat()
    }
    
    save_settings(settings)

def get_time_limit(app_name):
    """Obtiene el lÃ­mite de tiempo de una app."""
    settings = load_settings()
    return settings.get('time_limits', {}).get(app_name, None)

def update_app_usage(app_name, seconds=1):
    """Actualiza el tiempo de uso de una app."""
    settings = load_settings()
    
    if 'time_limits' not in settings or app_name not in settings['time_limits']:
        return
    
    settings['time_limits'][app_name]['used'] += seconds
    save_settings(settings)

def reset_daily_usage():
    """Reinicia el contador diario de uso."""
    settings = load_settings()
    
    if 'time_limits' not in settings:
        return
    
    for app in settings['time_limits']:
        settings['time_limits'][app]['used'] = 0
        settings['time_limits'][app]['last_reset'] = datetime.now().isoformat()
    
    save_settings(settings)

