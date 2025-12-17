"""
Nueva interfaz de usuario mejorada de Guardian.
Diseño moderno, responsive y visualmente atractivo.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
from src.features.enhanced_ui import (
    COLORS, ModernButton, StatCard, ModernTabbedUI, 
    ProgressBar, TimeTracker, FocusTimer, NotificationBadge
)
from src.features.advanced_analytics import (
    ProductivityAnalyzer, BreakReminderSystem, HealthMonitor, InsightGenerator
)
from src.core.monitor import monitor_apps
from src.utils.settings_manager import (
    load_settings, save_settings, get_session_stats, get_blocked_apps
)


class ModernGuardianUI:
    """Interfaz moderna de Guardian."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Guardian - Digital Wellness")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['dark'])
        
        # Sistemas internos
        self.monitor_running = False
        self.analyzer = ProductivityAnalyzer()
        self.break_system = BreakReminderSystem()
        self.health_monitor = HealthMonitor()
        self.focus_timer = FocusTimer()
        self.time_tracker = TimeTracker()
        self.insight_gen = InsightGenerator(self.analyzer)
        
        self.setup_ui()
        self.update_widgets()

    def setup_ui(self):
        """Configura la interfaz."""
        # Header con gradiente
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header, bg=COLORS['primary'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(title_frame, text="🛡️ GUARDIAN", font=("Segoe UI", 24, "bold"),
                fg=COLORS['text'], bg=COLORS['primary']).pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="Digital Wellness System",
                font=("Segoe UI", 10), fg=COLORS['light'], 
                bg=COLORS['primary']).pack(side=tk.LEFT, padx=20)
        
        # Notificación
        self.notification_badge = NotificationBadge(title_frame)
        self.notification_badge.pack(side=tk.RIGHT)
        
        # Interfaz tabulada
        self.tabbed_ui = ModernTabbedUI(self.root)
        
        # Crear pestañas
        self.dashboard_tab = self.tabbed_ui.add_tab('dashboard', '📊 Dashboard')
        self.focus_tab = self.tabbed_ui.add_tab('focus', '⏱️ Focus')
        self.health_tab = self.tabbed_ui.add_tab('health', '❤️ Health')
        self.insights_tab = self.tabbed_ui.add_tab('insights', '💡 Insights')
        self.settings_tab = self.tabbed_ui.add_tab('settings', '⚙️ Settings')
        
        self.setup_dashboard_tab()
        self.setup_focus_tab()
        self.setup_health_tab()
        self.setup_insights_tab()
        self.setup_settings_tab()
        
        # Mostrar dashboard por defecto
        self.tabbed_ui.show_tab('dashboard')

    def setup_dashboard_tab(self):
        """Configura la pestaña de dashboard."""
        # Cards de estadísticas principales
        stats_frame = tk.Frame(self.dashboard_tab, bg=COLORS['dark'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Estadísticas
        self.blocks_card = StatCard(stats_frame, title="Bloques Hoy", value="0",
                                   icon="🚫", color=COLORS['danger'],
                                   width=280, height=120)
        self.blocks_card.pack(side=tk.LEFT, padx=5)
        
        self.focus_card = StatCard(stats_frame, title="Tiempo de Enfoque",
                                  value="0 min", icon="⏱️", color=COLORS['success'],
                                  width=280, height=120)
        self.focus_card.pack(side=tk.LEFT, padx=5)
        
        self.score_card = StatCard(stats_frame, title="Productividad",
                                  value="0%", icon="📈", color=COLORS['primary'],
                                  width=280, height=120)
        self.score_card.pack(side=tk.LEFT, padx=5)
        
        # Barra de progreso
        progress_label = tk.Label(self.dashboard_tab, text="Enfoque del Día",
                                 font=("Segoe UI", 11, "bold"),
                                 fg=COLORS['text'], bg=COLORS['dark'])
        progress_label.pack(pady=(20, 5), padx=20, anchor=tk.W)
        
        self.progress_bar = ProgressBar(self.dashboard_tab, width=400, height=15,
                                       bg_color=COLORS['success'])
        self.progress_bar.pack(pady=5, padx=20)
        
        # Log de actividad
        log_frame = tk.Frame(self.dashboard_tab, bg=COLORS['dark'])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(log_frame, text="Actividad Reciente", font=("Segoe UI", 12, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack(anchor=tk.W, pady=(0, 10))
        
        self.activity_log = tk.Text(log_frame, bg=COLORS['card_bg'], fg=COLORS['text'],
                                   font=("Courier New", 10), height=10, width=80,
                                   relief=tk.FLAT)
        self.activity_log.pack(fill=tk.BOTH, expand=True)
        self.activity_log.config(state=tk.DISABLED)
        
        # Controles
        control_frame = tk.Frame(self.dashboard_tab, bg=COLORS['dark'])
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_start = tk.Button(control_frame, text="▶ Iniciar", 
                                  command=self.start_guardian,
                                  bg=COLORS['success'], fg=COLORS['text'],
                                  font=("Segoe UI", 11, "bold"),
                                  relief=tk.FLAT, padx=20, pady=10)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = tk.Button(control_frame, text="⏹ Detener",
                                 command=self.stop_guardian,
                                 bg=COLORS['danger'], fg=COLORS['text'],
                                 font=("Segoe UI", 11, "bold"),
                                 relief=tk.FLAT, padx=20, pady=10)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

    def setup_focus_tab(self):
        """Configura la pestaña de enfoque."""
        # Timer
        timer_frame = tk.Frame(self.focus_tab, bg=COLORS['dark'])
        timer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=40)
        
        tk.Label(timer_frame, text="Pomodoro Timer", font=("Segoe UI", 16, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack()
        
        self.timer_display = tk.Label(timer_frame, text="25:00",
                                     font=("Segoe UI", 72, "bold"),
                                     fg=COLORS['primary'], bg=COLORS['dark'])
        self.timer_display.pack(pady=30)
        
        # Controles del timer
        btn_frame = tk.Frame(timer_frame, bg=COLORS['dark'])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="▶ Iniciar", command=self.start_focus_timer,
                 bg=COLORS['success'], fg=COLORS['text'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                 padx=15, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="⏸ Pausar", command=self.pause_focus_timer,
                 bg=COLORS['warning'], fg=COLORS['text'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                 padx=15, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="🔄 Reiniciar", command=self.reset_focus_timer,
                 bg=COLORS['secondary'], fg=COLORS['text'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                 padx=15, pady=10).pack(side=tk.LEFT, padx=10)
        
        # Sugerencia de descanso
        self.break_suggestion = tk.Label(self.focus_tab, text="",
                                        font=("Segoe UI", 12),
                                        fg=COLORS['warning'], bg=COLORS['dark'],
                                        wraplength=600)
        self.break_suggestion.pack(pady=20)

    def setup_health_tab(self):
        """Configura la pestaña de salud."""
        health_frame = tk.Frame(self.health_tab, bg=COLORS['dark'])
        health_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(health_frame, text="Salud Digital", font=("Segoe UI", 16, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack(pady=(0, 20))
        
        # Score de salud
        self.health_score = tk.Label(health_frame, text="0", font=("Segoe UI", 48, "bold"),
                                    fg=COLORS['success'], bg=COLORS['dark'])
        self.health_score.pack(pady=10)
        
        tk.Label(health_frame, text="/100", font=("Segoe UI", 14),
                fg=COLORS['light'], bg=COLORS['dark']).pack()
        
        # Recomendaciones
        tk.Label(health_frame, text="Recomendaciones", font=("Segoe UI", 12, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack(pady=(30, 10), anchor=tk.W)
        
        self.health_recommendations = tk.Text(health_frame, bg=COLORS['card_bg'],
                                             fg=COLORS['text'], font=("Segoe UI", 11),
                                             height=10, relief=tk.FLAT,
                                             wrap=tk.WORD)
        self.health_recommendations.pack(fill=tk.BOTH, expand=True)
        self.health_recommendations.config(state=tk.DISABLED)

    def setup_insights_tab(self):
        """Configura la pestaña de insights."""
        insights_frame = tk.Frame(self.insights_tab, bg=COLORS['dark'])
        insights_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(insights_frame, text="Insights Personalizados", 
                font=("Segoe UI", 16, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack(pady=(0, 20))
        
        self.insights_text = tk.Text(insights_frame, bg=COLORS['card_bg'],
                                    fg=COLORS['text'], font=("Segoe UI", 11),
                                    relief=tk.FLAT, wrap=tk.WORD)
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        self.insights_text.config(state=tk.DISABLED)

    def setup_settings_tab(self):
        """Configura la pestaña de configuración."""
        settings_frame = tk.Frame(self.settings_tab, bg=COLORS['dark'])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(settings_frame, text="Configuración", font=("Segoe UI", 16, "bold"),
                fg=COLORS['text'], bg=COLORS['dark']).pack(pady=(0, 20), anchor=tk.W)
        
        # Opciones
        tk.Label(settings_frame, text="Duración Pomodoro (minutos):",
                font=("Segoe UI", 11), fg=COLORS['text'],
                bg=COLORS['dark']).pack(anchor=tk.W, pady=(10, 5))
        
        self.pomodoro_spinbox = tk.Spinbutton(settings_frame, from_=5, to=60,
                                             width=10, font=("Segoe UI", 11),
                                             bg=COLORS['card_bg'], fg=COLORS['text'])
        self.pomodoro_spinbox.set(25)
        self.pomodoro_spinbox.pack(anchor=tk.W)
        
        # Botón guardar
        tk.Button(settings_frame, text="💾 Guardar Configuración",
                 command=self.save_settings,
                 bg=COLORS['primary'], fg=COLORS['text'],
                 font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                 padx=20, pady=10).pack(pady=30, anchor=tk.W)

    def update_widgets(self):
        """Actualiza los widgets regularmente."""
        # Actualizar statisticas
        stats = self.analyzer.get_daily_stats()
        health = self.health_monitor.get_health_score()
        
        # Actualizar cards
        self.blocks_card.pack_forget()
        self.blocks_card = StatCard(self.dashboard_tab, 
                                   title="Bloques Hoy", 
                                   value=str(stats['blocks_today']),
                                   icon="🚫", color=COLORS['danger'],
                                   width=280, height=120)
        self.blocks_card.pack(side=tk.LEFT, padx=5)
        
        # Health score
        self.health_score.config(text=str(health))
        
        # Actualizar barra de progreso
        progress = min(100, (stats['focus_time_minutes'] / 120) * 100)
        self.progress_bar.set_progress(int(progress))
        
        # Sugerencia de descanso
        if self.break_system.should_take_break():
            self.break_suggestion.config(text=self.break_system.get_break_suggestion())
            self.notification_badge.update_count(1)
        
        # Timer
        self.timer_display.config(text=self.focus_timer.get_display_time())
        
        # Llamar nuevamente
        self.root.after(1000, self.update_widgets)

    def start_guardian(self):
        """Inicia Guardian."""
        self.monitor_running = True
        self.btn_start.config(state=tk.DISABLED, bg='#95a5a6')
        self.btn_stop.config(state=tk.NORMAL, bg=COLORS['danger'])
        self.time_tracker.start_session()
        threading.Thread(target=self.monitor_loop, daemon=True).start()
        self.log_activity("✓ Guardian iniciado - Monitoreando...")

    def stop_guardian(self):
        """Detiene Guardian."""
        self.monitor_running = False
        self.btn_start.config(state=tk.NORMAL, bg=COLORS['success'])
        self.btn_stop.config(state=tk.DISABLED, bg='#95a5a6')
        duration = self.time_tracker.end_session()
        self.health_monitor.add_screen_time(int(duration) if duration else 0)
        self.log_activity(f"⏹ Guardian detenido - Sesión: {int(duration) if duration else 0} min")

    def monitor_loop(self):
        """Loop de monitoreo."""
        while self.monitor_running:
            # Aquí iría la lógica de monitoreo real
            self.root.after(100)

    def start_focus_timer(self):
        """Inicia el timer de enfoque."""
        self.focus_timer.start()

    def pause_focus_timer(self):
        """Pausa el timer."""
        self.focus_timer.pause()

    def reset_focus_timer(self):
        """Reinicia el timer."""
        self.focus_timer.reset()

    def save_settings(self):
        """Guarda la configuración."""
        pomodoro_time = int(self.pomodoro_spinbox.get())
        self.focus_timer = FocusTimer(pomodoro_time, pomodoro_time // 5)
        self.log_activity(f"⚙️ Configuración guardada - Pomodoro: {pomodoro_time}min")

    def log_activity(self, message):
        """Registra una actividad."""
        self.activity_log.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activity_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.activity_log.see(tk.END)
        self.activity_log.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGuardianUI(root)
    root.mainloop()
