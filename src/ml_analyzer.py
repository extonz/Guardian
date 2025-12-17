"""
AnÃ¡lisis de patrones de distracciÃ³n con ML bÃ¡sico.
Predice cuÃ¡ndo es mÃ¡s probable distraerse.
"""

from datetime import datetime, timedelta
from src.settings_manager import load_stats
from collections import defaultdict
import statistics

def analyze_distraction_patterns():
    """Analiza patrones de cuÃ¡ndo ocurren distracciones."""
    stats = load_stats()
    blocks = stats.get('blocks', [])
    
    if not blocks:
        return None
    
    # Agrupar por hora del dÃ­a
    hourly_blocks = defaultdict(int)
    for block in blocks:
        try:
            time_str = block['timestamp'].split('T')[1]
            hour = int(time_str.split(':')[0])
            hourly_blocks[hour] += 1
        except:
            continue
    
    # Agrupar por dÃ­a de la semana
    daily_blocks = defaultdict(int)
    for block in blocks:
        try:
            date_str = block['timestamp'].split('T')[0]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            daily_blocks[day_name] += 1
        except:
            continue
    
    # Encontrar picos
    peak_hour = max(hourly_blocks, key=hourly_blocks.get) if hourly_blocks else None
    peak_day = max(daily_blocks, key=daily_blocks.get) if daily_blocks else None
    
    return {
        'hourly': dict(hourly_blocks),
        'daily': dict(daily_blocks),
        'peak_hour': peak_hour,
        'peak_day': peak_day,
        'high_risk_hours': [h for h, count in hourly_blocks.items() if count > statistics.mean(hourly_blocks.values()) if hourly_blocks],
    }

def predict_distraction_risk():
    """Predice el riesgo de distracciÃ³n en la hora actual."""
    patterns = analyze_distraction_patterns()
    if not patterns:
        return 'bajo', 50
    
    current_hour = datetime.now().hour
    current_day = datetime.now().strftime("%A")
    
    hour_risk = patterns['hourly'].get(current_hour, 0)
    day_risk = patterns['daily'].get(current_day, 0)
    
    # Calcular score de 0-100
    avg_hourly = sum(patterns['hourly'].values()) / len(patterns['hourly']) if patterns['hourly'] else 0
    avg_daily = sum(patterns['daily'].values()) / len(patterns['daily']) if patterns['daily'] else 0
    
    hour_score = (hour_risk / avg_hourly * 50) if avg_hourly > 0 else 25
    day_score = (day_risk / avg_daily * 50) if avg_daily > 0 else 25
    
    total_score = min(100, hour_score + day_score)
    
    if total_score >= 75:
        risk_level = 'muy alto'
    elif total_score >= 50:
        risk_level = 'alto'
    elif total_score >= 25:
        risk_level = 'medio'
    else:
        risk_level = 'bajo'
    
    return risk_level, int(total_score)

def get_best_focus_times():
    """Retorna las mejores horas para enfocarse (menos distracciones)."""
    patterns = analyze_distraction_patterns()
    if not patterns or not patterns['hourly']:
        return None
    
    sorted_hours = sorted(patterns['hourly'].items(), key=lambda x: x[1])
    best_hours = [hour for hour, count in sorted_hours[:3]]
    
    return best_hours

def get_worst_focus_times():
    """Retorna las peores horas para enfocarse (mÃ¡s distracciones)."""
    patterns = analyze_distraction_patterns()
    if not patterns or not patterns['hourly']:
        return None
    
    sorted_hours = sorted(patterns['hourly'].items(), key=lambda x: x[1], reverse=True)
    worst_hours = [hour for hour, count in sorted_hours[:3]]
    
    return worst_hours

def get_app_correlation(app_name):
    """Analiza quÃ© apps suelen estar abiertas cuando se abre una app bloqueada."""
    stats = load_stats()
    blocks = stats.get('blocks', [])
    
    # Encontrar bloques de esta app
    app_blocks = [b for b in blocks if b.get('app') == app_name]
    
    if not app_blocks:
        return {}
    
    # Esto serÃ­a mÃ¡s complejo con datos reales
    return {'total_blocks': len(app_blocks)}

def suggest_strategy():
    """Sugiere estrategia basada en patrones."""
    best_times = get_best_focus_times()
    worst_times = get_worst_focus_times()
    risk, score = predict_distraction_risk()
    
    suggestions = []
    
    if score >= 75:
        suggestions.append("âš ï¸ Riesgo MUY ALTO - Considera tomar un descanso")
    elif score >= 50:
        suggestions.append("âš ï¸ Riesgo ALTO - SÃ© extra cuidadoso")
    
    if best_times:
        suggestions.append(f"âœ… Mejores horarios: {':'.join([f'{h:02d}:00' for h in sorted(best_times)])}")
    
    if worst_times:
        suggestions.append(f"âŒ Horarios peligrosos: {':'.join([f'{h:02d}:00' for h in sorted(worst_times)])}")
    
    return suggestions

