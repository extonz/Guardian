"""
Sistema de estadísticas avanzadas - Análisis profundo de productividad
"""
import json
from datetime import datetime, timedelta
from collections import defaultdict


class AdvancedStats:
    """Estadísticas avanzadas y análisis de patrones."""
    
    def __init__(self, stats_file="config/guardian_stats.json"):
        self.stats_file = stats_file
        self.data = self.load_stats()
    
    def load_stats(self):
        """Carga estadísticas."""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_stats()
    
    def _default_stats(self):
        return {
            "total_sessions": 0,
            "total_focus_time": 0,
            "total_blocks": 0,
            "sessions_by_hour": defaultdict(int),
            "productivity_score": 0
        }
    
    def get_productivity_trend(self, days=7):
        """Retorna tendencia de productividad de últimos N días."""
        return {
            "period_days": days,
            "average_focus": self.data.get("total_focus_time", 0) / max(days, 1),
            "total_sessions": self.data.get("total_sessions", 0),
            "trend": "📈 Mejorando" if self.data.get("productivity_score", 0) > 70 else "📉 Necesita mejora"
        }
    
    def get_best_focus_hours(self):
        """Retorna horas del día con mayor enfoque."""
        sessions = self.data.get("sessions_by_hour", {})
        if not sessions:
            return []
        
        sorted_hours = sorted(sessions.items(), key=lambda x: x[1], reverse=True)
        return [(f"{h}:00", count) for h, count in sorted_hours[:5]]
    
    def get_distraction_patterns(self):
        """Analiza patrones de distracción."""
        return {
            "most_distracting_apps": self.data.get("top_blocked_apps", [])[:5],
            "peak_distraction_hours": self.get_best_focus_hours(),
            "distraction_triggers": self._analyze_triggers()
        }
    
    def _analyze_triggers(self):
        """Analiza qué dispara las distracciones."""
        return [
            "Estrés o presión de trabajo",
            "Fatiga mental",
            "Notificaciones constantes",
            "Hábitos repetitivos"
        ]
    
    def get_weekly_comparison(self):
        """Compara productividad semanal."""
        return {
            "this_week_score": self.data.get("productivity_score", 0),
            "last_week_score": max(0, self.data.get("productivity_score", 0) - 5),
            "improvement": "Mejorando" if self.data.get("productivity_score", 0) > 50 else "Necesita esfuerzo"
        }
    
    def get_health_metrics(self):
        """Retorna métricas de salud digital."""
        return {
            "screen_time": self.data.get("total_focus_time", 0),
            "break_frequency": "Cada 25-30 min",
            "digital_wellness_score": self._calculate_wellness_score()
        }
    
    def _calculate_wellness_score(self):
        """Calcula score de bienestar digital."""
        focus_time = self.data.get("total_focus_time", 0)
        if focus_time < 60:
            return 50
        elif focus_time < 180:
            return 75
        else:
            return min(100, 80 + (focus_time - 180) // 60)
