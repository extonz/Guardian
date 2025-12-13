"""
Análisis avanzado de patrones de comportamiento y productividad.
"""

from datetime import datetime, timedelta
from collections import defaultdict

class ProductivityAnalyzer:
    """Analiza patrones de productividad."""
    def __init__(self):
        self.block_events = []
        self.focus_sessions = []
        self.time_of_day_stats = defaultdict(int)

    def record_block(self, app_name, timestamp=None):
        """Registra un bloqueo."""
        if timestamp is None:
            timestamp = datetime.now()
        self.block_events.append({
            'app': app_name,
            'time': timestamp,
            'hour': timestamp.hour
        })
        self.time_of_day_stats[timestamp.hour] += 1

    def record_focus_session(self, duration_minutes, quality=1.0):
        """Registra una sesión de enfoque."""
        self.focus_sessions.append({
            'duration': duration_minutes,
            'quality': quality,
            'timestamp': datetime.now()
        })

    def get_peak_distraction_hour(self):
        """Retorna la hora del día con más distracciones."""
        if not self.time_of_day_stats:
            return None
        return max(self.time_of_day_stats.items(), key=lambda x: x[1])[0]

    def get_most_blocked_app(self):
        """Retorna la app más bloqueada."""
        if not self.block_events:
            return None
        app_counts = defaultdict(int)
        for event in self.block_events:
            app_counts[event['app']] += 1
        return max(app_counts.items(), key=lambda x: x[1])[0]

    def get_productivity_score(self):
        """Calcula un score de productividad (0-100)."""
        if not self.focus_sessions:
            return 0
        
        total_quality = sum(s['quality'] for s in self.focus_sessions)
        avg_quality = total_quality / len(self.focus_sessions)
        
        total_duration = sum(s['duration'] for s in self.focus_sessions)
        duration_score = min(100, (total_duration / 120) * 100)  # Base 2 horas
        
        return int((avg_quality * 100 + duration_score) / 2)

    def get_daily_stats(self):
        """Retorna estadísticas del día."""
        today = datetime.now().date()
        today_blocks = [e for e in self.block_events 
                       if e['time'].date() == today]
        today_sessions = [s for s in self.focus_sessions 
                         if s['timestamp'].date() == today]
        
        total_focus = sum(s['duration'] for s in today_sessions)
        
        return {
            'blocks_today': len(today_blocks),
            'focus_time_minutes': total_focus,
            'sessions_today': len(today_sessions),
            'unique_apps_blocked': len(set(e['app'] for e in today_blocks))
        }

    def get_weekly_trends(self):
        """Retorna tendencias de la semana."""
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        daily_stats = defaultdict(lambda: {'blocks': 0, 'focus': 0})
        
        for event in self.block_events:
            if event['time'].date() >= week_start:
                day = event['time'].date()
                daily_stats[day]['blocks'] += 1
        
        for session in self.focus_sessions:
            if session['timestamp'].date() >= week_start:
                day = session['timestamp'].date()
                daily_stats[day]['focus'] += session['duration']
        
        return dict(daily_stats)


class BreakReminderSystem:
    """Sistema inteligente de recordatorios de descanso."""
    def __init__(self, focus_minutes=50):
        self.focus_time = focus_minutes
        self.last_break = datetime.now()
        self.consecutive_focus = 0

    def should_take_break(self):
        """Determina si es momento de un descanso."""
        time_since_break = (datetime.now() - self.last_break).total_seconds() / 60
        return time_since_break >= self.focus_time

    def record_break(self):
        """Registra que se tomó un descanso."""
        self.last_break = datetime.now()
        self.consecutive_focus = 0

    def get_break_suggestion(self):
        """Retorna una sugerencia de descanso."""
        suggestions = [
            "💧 Bebe agua - Mantente hidratado",
            "👀 Mira hacia el horizonte - Descansa la vista",
            "🧘 Respira profundamente - Relájate",
            "🚶 Camina un poco - Mueve las piernas",
            "🎵 Escucha música - Relaja tu mente",
        ]
        return suggestions[self.consecutive_focus % len(suggestions)]

    def get_time_until_break(self):
        """Retorna minutos hasta el próximo descanso recomendado."""
        time_since_break = (datetime.now() - self.last_break).total_seconds() / 60
        return max(0, int(self.focus_time - time_since_break))


class HealthMonitor:
    """Monitorea la salud digital del usuario."""
    def __init__(self):
        self.screen_time_sessions = []
        self.break_count = 0
        self.posture_warnings = 0

    def add_screen_time(self, minutes):
        """Registra tiempo de pantalla."""
        self.screen_time_sessions.append({
            'duration': minutes,
            'timestamp': datetime.now()
        })

    def log_break(self):
        """Registra que el usuario se tomó un descanso."""
        self.break_count += 1

    def log_posture_warning(self):
        """Registra una advertencia de postura."""
        self.posture_warnings += 1

    def get_health_score(self):
        """Calcula un score de salud digital (0-100)."""
        today = datetime.now().date()
        today_sessions = [s for s in self.screen_time_sessions 
                         if s['timestamp'].date() == today]
        total_screen_time = sum(s['duration'] for s in today_sessions)
        
        # Puntos negativos: tiempo de pantalla (100+ = 0 puntos)
        screen_score = max(0, 100 - (total_screen_time / 60) * 10)
        
        # Puntos positivos: descansos y postura
        break_score = min(100, self.break_count * 10)
        posture_score = max(0, 100 - self.posture_warnings * 5)
        
        return int((screen_score + break_score + posture_score) / 3)

    def get_health_recommendations(self):
        """Retorna recomendaciones de salud."""
        recommendations = []
        
        health = self.get_health_score()
        
        if health < 40:
            recommendations.append("⚠️ Toma descansos más frecuentes")
            recommendations.append("👀 Aplica la regla 20-20-20 (cada 20 min, mira 20 seg a 20 pies)")
        
        return recommendations


class InsightGenerator:
    """Genera insights personalizados."""
    def __init__(self, analyzer: ProductivityAnalyzer):
        self.analyzer = analyzer

    def generate_daily_insights(self):
        """Genera insights del día."""
        stats = self.analyzer.get_daily_stats()
        insights = []
        
        if stats['blocks_today'] > 5:
            insights.append(f"🎯 Hoy has tenido {stats['blocks_today']} distracciones. ¡Mantén el enfoque!")
        
        if stats['focus_time_minutes'] > 120:
            insights.append(f"⭐ ¡Excelente! Has dedicado {int(stats['focus_time_minutes'])} minutos a enfoque.")
        
        most_blocked = self.analyzer.get_most_blocked_app()
        if most_blocked:
            insights.append(f"📱 Hoy tu mayor distracción ha sido: {most_blocked}")
        
        return insights

    def generate_recommendations(self):
        """Genera recomendaciones personalizadas."""
        peak_hour = self.analyzer.get_peak_distraction_hour()
        recommendations = []
        
        if peak_hour:
            recommendations.append(f"🕐 Tienes más distracciones a las {peak_hour}:00. Planifica sesiones de enfoque en otras horas.")
        
        score = self.analyzer.get_productivity_score()
        if score < 50:
            recommendations.append("💪 Intenta con sesiones más cortas de Pomodoro (15-20 min)")
        
        return recommendations
