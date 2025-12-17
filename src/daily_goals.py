"""
Sistema de metas diarias - Establece y monitorea objetivos de productividad
"""
import json
import os
from datetime import datetime, timedelta


class DailyGoalsManager:
    """Gestiona metas diarias y su progreso."""
    
    def __init__(self, config_path="config/daily_goals.json"):
        self.config_path = config_path
        self.goals = self.load_goals()
    
    def load_goals(self):
        """Carga las metas del archivo."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._default_goals()
        return self._default_goals()
    
    def _default_goals(self):
        """Retorna metas por defecto."""
        return {
            "daily": {
                "focus_time": 120,  # minutos
                "blocks_limit": 10,
                "break_time": 30,
                "active_tasks": 3
            }
        }
    
    def save_goals(self):
        """Guarda las metas."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.goals, f, indent=2)
    
    def set_goal(self, goal_type, value):
        """Establece una meta."""
        self.goals["daily"][goal_type] = value
        self.save_goals()
        return f"Meta '{goal_type}' establecida en {value}"
    
    def get_goals(self):
        """Retorna todas las metas."""
        return self.goals["daily"]
    
    def check_goal_progress(self, stats):
        """Verifica el progreso de las metas."""
        goals = self.goals["daily"]
        progress = {
            "focus_time": {
                "target": goals["focus_time"],
                "current": stats.get("focus_time_minutes", 0),
                "percentage": int((stats.get("focus_time_minutes", 0) / goals["focus_time"]) * 100) if goals["focus_time"] > 0 else 0
            },
            "blocks": {
                "limit": goals["blocks_limit"],
                "current": stats.get("blocks_today", 0),
                "within_limit": stats.get("blocks_today", 0) <= goals["blocks_limit"]
            }
        }
        return progress
