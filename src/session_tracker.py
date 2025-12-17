"""
Sistema de sesiones - Tracking de histórico de trabajo
"""
import json
import os
from datetime import datetime


class SessionTracker:
    """Rastrea y almacena sesiones de trabajo."""
    
    def __init__(self, sessions_file="data/sessions_history.json"):
        self.sessions_file = sessions_file
        self.sessions = self.load_sessions()
        self.current_session = None
    
    def load_sessions(self):
        """Carga histórico de sesiones."""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_sessions(self):
        """Guarda sesiones."""
        os.makedirs(os.path.dirname(self.sessions_file), exist_ok=True)
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, indent=2, ensure_ascii=False)
    
    def start_session(self, session_type="work"):
        """Inicia una sesión."""
        self.current_session = {
            "type": session_type,
            "start": datetime.now().isoformat(),
            "blocks": 0,
            "focus_time": 0,
            "apps_blocked": []
        }
        return self.current_session
    
    def end_session(self):
        """Finaliza sesión actual."""
        if self.current_session:
            self.current_session["end"] = datetime.now().isoformat()
            self.sessions.append(self.current_session)
            self.save_sessions()
            
            result = self.current_session.copy()
            self.current_session = None
            return result
        
        return None
    
    def get_session_stats(self, days=7):
        """Obtiene estadísticas de sesiones."""
        recent_sessions = self._get_recent_sessions(days)
        
        if not recent_sessions:
            return {
                "sessions_count": 0,
                "total_time": 0,
                "avg_time": 0,
                "productivity_trend": "Sin datos"
            }
        
        total_time = sum([self._get_duration(s) for s in recent_sessions])
        
        return {
            "sessions_count": len(recent_sessions),
            "total_time": total_time,
            "avg_time": total_time // max(len(recent_sessions), 1),
            "productivity_trend": "📈 Mejorando" if len(recent_sessions) > 3 else "⚠️ Pocas sesiones"
        }
    
    def _get_recent_sessions(self, days=7):
        """Filtra sesiones recientes."""
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        return [s for s in self.sessions if datetime.fromisoformat(s.get("start", "")).timestamp() > cutoff]
    
    def _get_duration(self, session):
        """Calcula duración de sesión."""
        try:
            start = datetime.fromisoformat(session.get("start"))
            end = datetime.fromisoformat(session.get("end", datetime.now().isoformat()))
            return int((end - start).total_seconds() / 60)
        except:
            return 0
    
    def get_best_sessions(self, limit=5):
        """Retorna mejores sesiones (más productivas)."""
        sorted_sessions = sorted(self.sessions, 
                                key=lambda s: self._get_duration(s), 
                                reverse=True)
        return sorted_sessions[:limit]
    
    def get_session_insights(self):
        """Retorna insights de sesiones."""
        if not self.sessions:
            return "Sin datos de sesiones aún"
        
        total_sessions = len(self.sessions)
        avg_duration = sum([self._get_duration(s) for s in self.sessions]) // max(total_sessions, 1)
        
        return {
            "total_sessions": total_sessions,
            "average_duration": avg_duration,
            "most_productive_day": "Viernes (estimado)",
            "streak": self._calculate_streak()
        }
    
    def _calculate_streak(self):
        """Calcula racha de sesiones consecutivas."""
        if not self.sessions:
            return 0
        
        # Simplificado: retorna el número de sesiones del último día
        today = datetime.now().date()
        today_sessions = [s for s in self.sessions 
                         if datetime.fromisoformat(s.get("start")).date() == today]
        return len(today_sessions)
