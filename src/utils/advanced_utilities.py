"""
Utilidades avanzadas para Guardian.
Incluye notificaciones, temas, y funcionalidades extra.
"""

import json
import os
from datetime import datetime, timedelta


class ThemeManager:
    """Gestor de temas para la aplicación."""
    
    THEMES = {
        'dark': {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'card_bg': '#34495e',
        },
        'light': {
            'primary': '#3498db',
            'secondary': '#2980b9',
            'success': '#2ecc71',
            'warning': '#e67e22',
            'danger': '#e74c3c',
            'dark': '#ffffff',
            'light': '#2c3e50',
            'card_bg': '#ecf0f1',
        },
        'ocean': {
            'primary': '#0ea5e9',
            'secondary': '#06b6d4',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'dark': '#0f172a',
            'light': '#f0f9ff',
            'card_bg': '#1e293b',
        }
    }

    @classmethod
    def get_theme(cls, name='dark'):
        """Retorna un tema específico."""
        return cls.THEMES.get(name, cls.THEMES['dark'])

    @classmethod
    def list_themes(cls):
        """Lista todos los temas disponibles."""
        return list(cls.THEMES.keys())


class NotificationCenter:
    """Centro de notificaciones."""
    
    def __init__(self):
        self.notifications = []
        self.max_notifications = 5

    def add_notification(self, title, message, notification_type='info', duration=5):
        """Agrega una notificación."""
        notification = {
            'id': len(self.notifications),
            'title': title,
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now(),
            'duration': duration,
            'read': False
        }
        self.notifications.insert(0, notification)
        
        # Mantener límite
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]
        
        return notification['id']

    def mark_as_read(self, notification_id):
        """Marca una notificación como leída."""
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['read'] = True

    def get_unread_count(self):
        """Retorna la cantidad de notificaciones no leídas."""
        return sum(1 for n in self.notifications if not n['read'])

    def get_notifications(self):
        """Retorna todas las notificaciones."""
        return self.notifications


class SessionManager:
    """Gestor de sesiones de trabajo."""
    
    def __init__(self, storage_path='sessions.json'):
        self.storage_path = storage_path
        self.sessions = self.load_sessions()
        self.current_session = None

    def start_session(self, name, focus_time_minutes=25):
        """Inicia una nueva sesión."""
        self.current_session = {
            'id': len(self.sessions) + 1,
            'name': name,
            'start': datetime.now().isoformat(),
            'focus_time': focus_time_minutes,
            'completed': False,
            'blocks_during': 0,
            'notes': ''
        }
        return self.current_session

    def end_session(self, notes=''):
        """Finaliza la sesión actual."""
        if self.current_session:
            self.current_session['end'] = datetime.now().isoformat()
            self.current_session['notes'] = notes
            self.current_session['completed'] = True
            
            self.sessions.append(self.current_session)
            self.save_sessions()
            
            session = self.current_session
            self.current_session = None
            return session
        return None

    def get_session_duration(self):
        """Retorna la duración de la sesión actual en minutos."""
        if self.current_session and 'start' in self.current_session:
            start = datetime.fromisoformat(self.current_session['start'])
            duration = (datetime.now() - start).total_seconds() / 60
            return duration
        return 0

    def get_completed_sessions(self, days=1):
        """Retorna sesiones completadas de los últimos N días."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        return [s for s in self.sessions 
                if s['completed'] and s['end'] > cutoff]

    def save_sessions(self):
        """Guarda las sesiones en archivo."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            print(f"Error saving sessions: {e}")

    def load_sessions(self):
        """Carga las sesiones desde archivo."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading sessions: {e}")
        return []


class AchievementSystem:
    """Sistema de logros."""
    
    ACHIEVEMENTS = {
        'first_block': {
            'name': '🔒 Primer Bloqueo',
            'description': 'Bloquea una app por primera vez',
            'icon': '🔒'
        },
        'focus_warrior': {
            'name': '⚔️ Guerrero del Enfoque',
            'description': 'Completa 10 sesiones de enfoque',
            'icon': '⚔️'
        },
        'iron_will': {
            'name': '💪 Voluntad de Hierro',
            'description': 'Mantén una racha de 7 días sin distracciones',
            'icon': '💪'
        },
        'health_champion': {
            'name': '🏆 Campeón de Salud',
            'description': 'Obtén un score de salud de 80+',
            'icon': '🏆'
        },
        'night_owl': {
            'name': '🦉 Búho Nocturno',
            'description': 'Trabaja 3 horas después de las 10 PM',
            'icon': '🦉'
        },
        'early_bird': {
            'name': '🐦 Madrugador',
            'description': 'Trabaja 3 horas antes de las 7 AM',
            'icon': '🐦'
        }
    }

    def __init__(self):
        self.unlocked = set()

    def unlock_achievement(self, achievement_id):
        """Desbloquea un logro."""
        if achievement_id in self.ACHIEVEMENTS and achievement_id not in self.unlocked:
            self.unlocked.add(achievement_id)
            return self.ACHIEVEMENTS[achievement_id]
        return None

    def get_achievement(self, achievement_id):
        """Obtiene un logro específico."""
        return self.ACHIEVEMENTS.get(achievement_id)

    def get_all_achievements(self):
        """Retorna todos los logros."""
        return self.ACHIEVEMENTS

    def get_unlocked_achievements(self):
        """Retorna los logros desbloqueados."""
        return {id: self.ACHIEVEMENTS[id] for id in self.unlocked}

    def get_unlock_progress(self):
        """Retorna el progreso de desbloqueos."""
        total = len(self.ACHIEVEMENTS)
        unlocked = len(self.unlocked)
        percentage = (unlocked / total) * 100
        return {'unlocked': unlocked, 'total': total, 'percentage': percentage}


class BackupManager:
    """Gestor de copias de seguridad."""
    
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def create_backup(self, files_to_backup):
        """Crea una copia de seguridad."""
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        for file_path in files_to_backup:
            if os.path.exists(file_path):
                dest = os.path.join(backup_path, os.path.basename(file_path))
                if os.path.isfile(file_path):
                    shutil.copy2(file_path, dest)
                else:
                    shutil.copytree(file_path, dest)
        
        return backup_path

    def list_backups(self):
        """Lista todas las copias de seguridad."""
        if os.path.exists(self.backup_dir):
            return os.listdir(self.backup_dir)
        return []

    def restore_backup(self, backup_name, restore_path):
        """Restaura una copia de seguridad."""
        import shutil
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        if os.path.exists(backup_path):
            for item in os.listdir(backup_path):
                src = os.path.join(backup_path, item)
                dest = os.path.join(restore_path, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dest)
                else:
                    shutil.copytree(src, dest)
            return True
        return False


class ReportGenerator:
    """Generador de reportes personalizados."""
    
    @staticmethod
    def generate_weekly_report(analyzer, health_monitor):
        """Genera un reporte semanal."""
        trends = analyzer.get_weekly_trends()
        
        report = {
            'period': 'weekly',
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_blocks': sum(d['blocks'] for d in trends.values()),
                'total_focus': sum(d['focus'] for d in trends.values()),
                'health_score': health_monitor.get_health_score()
            },
            'daily_breakdown': trends
        }
        return report

    @staticmethod
    def generate_monthly_report(sessions, analyzer):
        """Genera un reporte mensual."""
        report = {
            'period': 'monthly',
            'generated': datetime.now().isoformat(),
            'total_sessions': len(sessions),
            'productivity_score': analyzer.get_productivity_score(),
            'insights': analyzer.get_daily_stats()
        }
        return report

    @staticmethod
    def export_report_to_json(report, filename):
        """Exporta un reporte a JSON."""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
