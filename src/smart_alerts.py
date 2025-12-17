"""
Sistema de alertas inteligentes - Notificaciones contextuales
"""
from datetime import datetime


class SmartAlerts:
    """Genera alertas inteligentes según contexto."""
    
    def __init__(self):
        self.alerts = []
    
    def check_productivity_alerts(self, stats):
        """Verifica y genera alertas de productividad."""
        alerts = []
        
        focus_time = stats.get("focus_time_minutes", 0)
        blocks = stats.get("blocks_today", 0)
        
        # Alerta 1: Poco tiempo de enfoque
        if focus_time < 30:
            alerts.append({
                "type": "focus_low",
                "message": "⚠️ Poco tiempo de enfoque hoy. ¡Intenta una sesión Pomodoro!",
                "severity": "medium",
                "action": "start_pomodoro"
            })
        
        # Alerta 2: Muchas distracciones
        if blocks > 15:
            alerts.append({
                "type": "too_many_distractions",
                "message": "🚨 Muchas distracciones detectadas. Considera modo 'Zen'",
                "severity": "high",
                "action": "start_zen_mode"
            })
        
        # Alerta 3: Pausa sugerida
        if focus_time > 90 and focus_time % 25 == 0:
            alerts.append({
                "type": "break_time",
                "message": "☕ Lleva trabajando {0} min. ¡Tómate un descanso!".format(focus_time),
                "severity": "low",
                "action": "take_break"
            })
        
        # Alerta 4: Hora de mejor enfoque
        current_hour = datetime.now().hour
        if current_hour in [9, 10, 11]:  # Mañana: mejor enfoque
            alerts.append({
                "type": "peak_hours",
                "message": "⏰ Es tu mejor hora para concentrarse. ¡Aprovecha!",
                "severity": "low",
                "action": None
            })
        
        return alerts
    
    def get_wellness_alert(self, stats):
        """Alerta sobre bienestar digital."""
        screen_time = stats.get("focus_time_minutes", 0)
        
        if screen_time > 240:
            return {
                "type": "wellness",
                "message": "💪 Has trabajado {0} minutos. Cuida tu vista y postura.".format(screen_time),
                "severity": "medium",
                "tips": [
                    "Mira lejos cada 20 minutos",
                    "Ajusta la iluminación",
                    "Estira tu cuello y espalda"
                ]
            }
        
        return None
    
    def get_daily_summary_alert(self, stats):
        """Resumen diario con alertas."""
        return {
            "title": "📊 Resumen de Hoy",
            "focus_time": stats.get("focus_time_minutes", 0),
            "blocks": stats.get("blocks_today", 0),
            "productivity_score": stats.get("productivity_score", 0),
            "status": "✅ Buen día" if stats.get("productivity_score", 0) > 70 else "⚠️ Día difícil"
        }
    
    def format_alert_message(self, alert):
        """Formatea alerta para mostrar."""
        return f"{alert.get('message', '')}\n\nAcción sugerida: {alert.get('action', 'No aplica')}"
