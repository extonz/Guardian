"""
Sistema de gamificaciÃ³n: badges, streaks, puntos, logros.
Motiva al usuario a mantener el foco.
"""

from datetime import datetime, timedelta
from src.settings_manager import load_settings, save_settings
import json

def get_or_create_gamification():
    """Crea/obtiene datos de gamificaciÃ³n."""
    settings = load_settings()
    if 'gamification' not in settings:
        settings['gamification'] = {
            'points': 0,
            'level': 1,
            'streak_days': 0,
            'last_streak_date': None,
            'badges': [],
            'achievements': [],
            'total_focus_hours': 0,
        }
        save_settings(settings)
    return settings['gamification']

def add_points(amount):
    """Agrega puntos y calcula el nuevo nivel."""
    settings = load_settings()
    settings['gamification']['points'] += amount
    
    # Calcular nivel: cada 1000 puntos = 1 nivel
    settings['gamification']['level'] = 1 + (settings['gamification']['points'] // 1000)
    save_settings(settings)
    return settings['gamification']

def update_streak():
    """Actualiza el streak de dÃ­as consecutivos sin distracciones."""
    settings = load_settings()
    gamif = settings['gamification']
    today = datetime.now().strftime("%Y-%m-%d")
    
    if gamif['last_streak_date'] is None:
        gamif['streak_days'] = 1
        gamif['last_streak_date'] = today
    elif gamif['last_streak_date'] != today:
        last_date = datetime.strptime(gamif['last_streak_date'], "%Y-%m-%d")
        today_date = datetime.now()
        
        if (today_date - last_date).days == 1:
            gamif['streak_days'] += 1
        else:
            gamif['streak_days'] = 1
        
        gamif['last_streak_date'] = today
    
    save_settings(settings)
    return gamif['streak_days']

def unlock_badge(badge_name):
    """Desbloquea un badge si no lo tiene."""
    settings = load_settings()
    gamif = settings['gamification']
    
    if badge_name not in gamif['badges']:
        gamif['badges'].append(badge_name)
        save_settings(settings)
        return True
    return False

def get_available_badges():
    """Retorna todos los badges disponibles."""
    return {
        'novice': {'name': 'ðŸ‘¶ Novato', 'description': 'Completar primer dÃ­a', 'requirement': lambda: True},
        'week_warrior': {'name': 'âš”ï¸ Guerrero Semanal', 'description': 'Mantener 7 dÃ­as de streak', 'requirement': lambda: get_streak() >= 7},
        'month_master': {'name': 'ðŸ‘‘ Maestro Mensual', 'description': '30 dÃ­as de streak', 'requirement': lambda: get_streak() >= 30},
        'focus_demon': {'name': 'ðŸ˜ˆ Demonio del Enfoque', 'description': '100 horas de enfoque', 'requirement': lambda: get_total_hours() >= 100},
        'blocker_king': {'name': 'ðŸš« Rey del Bloqueo', 'description': 'Bloquear 1000 apps', 'requirement': lambda: True},
        'midnight_warrior': {'name': 'ðŸŒ™ Guerrero Nocturno', 'description': 'SesiÃ³n de 2AM', 'requirement': lambda: datetime.now().hour >= 2},
        'marathon': {'name': 'ðŸƒ MaratÃ³n', 'description': '8 horas de enfoque', 'requirement': lambda: True},
        'perfectionist': {'name': 'âœ¨ Perfeccionista', 'description': 'Sin interrupciones en 1 hora', 'requirement': lambda: True},
    }

def check_and_unlock_badges():
    """Verifica y desbloquea badges automÃ¡ticamente."""
    gamif = get_or_create_gamification()
    badges = get_available_badges()
    new_badges = []
    
    for badge_id, badge_info in badges.items():
        try:
            if badge_id not in gamif['badges'] and badge_info['requirement']():
                if unlock_badge(badge_id):
                    new_badges.append(badge_info['name'])
        except:
            pass
    
    return new_badges

def get_streak():
    """Obtiene el streak actual."""
    gamif = get_or_create_gamification()
    return gamif['streak_days']

def get_points():
    """Obtiene los puntos actuales."""
    gamif = get_or_create_gamification()
    return gamif['points']

def get_level():
    """Obtiene el nivel actual."""
    gamif = get_or_create_gamification()
    return gamif['level']

def get_total_hours():
    """Obtiene total de horas de enfoque."""
    gamif = get_or_create_gamification()
    return gamif['total_focus_hours']

def add_focus_time(minutes):
    """Agrega tiempo de enfoque."""
    settings = load_settings()
    settings['gamification']['total_focus_hours'] += minutes / 60
    save_settings(settings)

def get_gamification_status():
    """Retorna estado completo de gamificaciÃ³n."""
    gamif = get_or_create_gamification()
    badges_dict = get_available_badges()
    
    badge_info = []
    for badge_id in gamif['badges']:
        if badge_id in badges_dict:
            badge_info.append(badges_dict[badge_id]['name'])
    
    return {
        'points': gamif['points'],
        'level': gamif['level'],
        'streak': gamif['streak_days'],
        'hours': round(gamif['total_focus_hours'], 1),
        'badges': badge_info,
        'progress_to_next_level': (gamif['points'] % 1000) / 10,  # 0-100%
    }

