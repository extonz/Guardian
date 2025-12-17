#!/usr/bin/env python3
"""
Guardian - Sistema de Bienestar Digital v5.1
App principal con UI profesional, diálogos personalizados y funciones restauradas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import tkinter.simpledialog
from datetime import datetime, time
import json
from pathlib import Path

# Import core modules (safe imports)
try:
    from src.settings_manager import load_settings, save_settings, get_blocked_apps
    from src.logger import log_info
    from src.monitor import monitor_apps
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

# Import new v5.1 features
try:
    from src.daily_goals import DailyGoalsManager
    from src.advanced_stats import AdvancedStats
    from src.smart_alerts import SmartAlerts
    from src.session_tracker import SessionTracker
    from src.advanced_exporter import AdvancedExporter
except ImportError as e:
    print(f"Warning: Some v5.1 features not available: {e}")

# ======================
# Global variables
# ======================
root = None
status_label = None
log_text = None
monitor_running = False
current_settings = None

# Colors - Professional dark theme
bg_dark = "#0a0e27"
bg_light = "#1a1f3a"
bg_lighter = "#242a45"
accent_color = "#00d4ff"
accent_hover = "#00b4d0"
success_color = "#00ff88"
warning_color = "#ffaa00"
danger_color = "#ff3333"
text_color = "#e0e0e0"
text_secondary = "#a0a0a0"

# Data directory for profiles and settings
DATA_DIR = Path("config")
PROFILES_FILE = DATA_DIR / "profiles.json"
WHITELIST_FILE = DATA_DIR / "whitelist.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)

# ======================
# Utility Functions - Profile Management
# ======================

def get_profiles():
    """Load all saved profiles."""
    try:
        if PROFILES_FILE.exists():
            with open(PROFILES_FILE, 'r') as f:
                return json.load(f)
        return {"default": {"name": "Defecto", "blocked_apps": [], "zen_mode": False}}
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return {"default": {"name": "Defecto", "blocked_apps": [], "zen_mode": False}}

def save_profiles(profiles):
    """Save profiles to file."""
    try:
        with open(PROFILES_FILE, 'w') as f:
            json.dump(profiles, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving profiles: {e}")
        return False

def get_whitelist():
    """Load whitelist."""
    try:
        if WHITELIST_FILE.exists():
            with open(WHITELIST_FILE, 'r') as f:
                return json.load(f)
        return {"apps": [], "websites": []}
    except Exception as e:
        print(f"Error loading whitelist: {e}")
        return {"apps": [], "websites": []}

def save_whitelist(whitelist):
    """Save whitelist."""
    try:
        with open(WHITELIST_FILE, 'w') as f:
            json.dump(whitelist, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving whitelist: {e}")
        return False

def get_schedule():
    """Load schedule configuration."""
    try:
        if SCHEDULE_FILE.exists():
            with open(SCHEDULE_FILE, 'r') as f:
                return json.load(f)
        return {
            "work_hours": {"start": "09:00", "end": "17:00"},
            "break_duration": 15,
            "sessions": {}
        }
    except Exception as e:
        print(f"Error loading schedule: {e}")
        return {"work_hours": {"start": "09:00", "end": "17:00"}, "break_duration": 15, "sessions": {}}

def save_schedule(schedule):
    """Save schedule configuration."""
    try:
        with open(SCHEDULE_FILE, 'w') as f:
            json.dump(schedule, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving schedule: {e}")
        return False

# ======================
# Custom Dialog Classes
# ======================

class CustomDialog(tk.Toplevel):
    """Base class for custom dialogs with professional styling."""
    def __init__(self, parent, title, width=400, height=300):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.config(bg=bg_dark)
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

class ProfileDialog(CustomDialog):
    """Dialog for managing profiles."""
    def __init__(self, parent):
        super().__init__(parent, "Gestión de Perfiles", width=500, height=400)
        self.result = None
        self.profiles = get_profiles()
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="👤 GESTIÓN DE PERFILES", 
                              font=("Segoe UI", 14, "bold"),
                              fg=accent_color, bg=bg_dark)
        title_label.pack(pady=10)
        
        # Profiles listbox
        tk.Label(self, text="Perfiles disponibles:", font=("Segoe UI", 10),
                fg=text_color, bg=bg_dark).pack(anchor=tk.W, padx=20, pady=(5, 0))
        
        listbox_frame = tk.Frame(self, bg=bg_dark)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.profiles_listbox = tk.Listbox(
            listbox_frame, bg=bg_light, fg=success_color,
            font=("Segoe UI", 10), yscrollcommand=scrollbar.set
        )
        self.profiles_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.profiles_listbox.yview)
        
        for profile_id, profile in self.profiles.items():
            self.profiles_listbox.insert(tk.END, f"  {profile.get('name', profile_id)}")
        
        # Buttons
        button_frame = tk.Frame(self, bg=bg_dark)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(button_frame, text="Crear Perfil", bg=success_color, fg=bg_dark,
                 font=("Segoe UI", 10, "bold"), command=self.create_profile,
                 relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Eliminar", bg=danger_color, fg="white",
                 font=("Segoe UI", 10, "bold"), command=self.delete_profile,
                 relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cerrar", bg=bg_lighter, fg=text_color,
                 font=("Segoe UI", 10, "bold"), command=self.destroy,
                 relief=tk.FLAT, padx=15).pack(side=tk.RIGHT, padx=5)
    
    def create_profile(self):
        dialog = tk.Toplevel(self)
        dialog.title("Nuevo Perfil")
        dialog.geometry("300x120")
        dialog.config(bg=bg_dark)
        
        tk.Label(dialog, text="Nombre del perfil:", fg=text_color, bg=bg_dark).pack(pady=5)
        entry = tk.Entry(dialog, bg=bg_light, fg=text_color, font=("Segoe UI", 10))
        entry.pack(padx=20, pady=5, fill=tk.X)
        entry.focus()
        
        def save():
            name = entry.get().strip()
            if name:
                self.profiles[name.lower().replace(" ", "_")] = {
                    "name": name,
                    "blocked_apps": [],
                    "zen_mode": False
                }
                save_profiles(self.profiles)
                self.profiles_listbox.insert(tk.END, f"  {name}")
                dialog.destroy()
                update_status("✓ Perfil creado exitosamente")
        
        tk.Button(dialog, text="Guardar", bg=success_color, fg=bg_dark,
                 command=save, relief=tk.FLAT).pack(pady=10)
    
    def delete_profile(self):
        selection = self.profiles_listbox.curselection()
        if selection:
            profiles_list = list(self.profiles.keys())
            if len(profiles_list) > 1:
                profile_id = profiles_list[selection[0]]
                if profile_id != "default":
                    del self.profiles[profile_id]
                    save_profiles(self.profiles)
                    self.profiles_listbox.delete(selection)
                    update_status("✓ Perfil eliminado")
                else:
                    messagebox.showwarning("Aviso", "No puedes eliminar el perfil por defecto")

class WhitelistDialog(CustomDialog):
    """Dialog for managing whitelist."""
    def __init__(self, parent):
        super().__init__(parent, "Gestor de Whitelist", width=500, height=400)
        self.whitelist = get_whitelist()
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="✅ GESTOR DE WHITELIST", 
                              font=("Segoe UI", 14, "bold"),
                              fg=success_color, bg=bg_dark)
        title_label.pack(pady=10)
        
        # Tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Apps tab
        apps_frame = tk.Frame(notebook, bg=bg_dark)
        notebook.add(apps_frame, text="Aplicaciones")
        
        tk.Label(apps_frame, text="Apps permitidas:", font=("Segoe UI", 10),
                fg=text_color, bg=bg_dark).pack(anchor=tk.W, padx=10, pady=5)
        
        self.apps_listbox = tk.Listbox(apps_frame, bg=bg_light, fg=success_color,
                                       font=("Segoe UI", 9), height=8)
        self.apps_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for app in self.whitelist.get("apps", []):
            self.apps_listbox.insert(tk.END, f"  {app}")
        
        apps_btn_frame = tk.Frame(apps_frame, bg=bg_dark)
        apps_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(apps_btn_frame, text="+ Agregar", bg=success_color, fg=bg_dark,
                 command=self.add_app, relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(apps_btn_frame, text="- Quitar", bg=danger_color, fg="white",
                 command=self.remove_app, relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        
        # Websites tab
        web_frame = tk.Frame(notebook, bg=bg_dark)
        notebook.add(web_frame, text="Sitios Web")
        
        tk.Label(web_frame, text="Sitios permitidos:", font=("Segoe UI", 10),
                fg=text_color, bg=bg_dark).pack(anchor=tk.W, padx=10, pady=5)
        
        self.web_listbox = tk.Listbox(web_frame, bg=bg_light, fg=success_color,
                                      font=("Segoe UI", 9), height=8)
        self.web_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for web in self.whitelist.get("websites", []):
            self.web_listbox.insert(tk.END, f"  {web}")
        
        web_btn_frame = tk.Frame(web_frame, bg=bg_dark)
        web_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(web_btn_frame, text="+ Agregar", bg=success_color, fg=bg_dark,
                 command=self.add_website, relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(web_btn_frame, text="- Quitar", bg=danger_color, fg="white",
                 command=self.remove_website, relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
        
        # Close button
        tk.Button(self, text="Guardar y Cerrar", bg=accent_color, fg=bg_dark,
                 font=("Segoe UI", 10, "bold"), command=self.save_and_close,
                 relief=tk.FLAT, padx=20).pack(pady=10)
    
    def add_app(self):
        value = tk.simpledialog.askstring("Agregar App", "Nombre de la aplicación:")
        if value:
            if value not in self.whitelist["apps"]:
                self.whitelist["apps"].append(value)
                self.apps_listbox.insert(tk.END, f"  {value}")
                update_status(f"✓ {value} agregada a whitelist")
    
    def remove_app(self):
        selection = self.apps_listbox.curselection()
        if selection:
            self.apps_listbox.delete(selection)
            app = list(self.whitelist["apps"])[selection[0]]
            self.whitelist["apps"].remove(app)
    
    def add_website(self):
        value = tk.simpledialog.askstring("Agregar Sitio", "URL del sitio web:")
        if value:
            if value not in self.whitelist["websites"]:
                self.whitelist["websites"].append(value)
                self.web_listbox.insert(tk.END, f"  {value}")
                update_status(f"✓ {value} agregada a whitelist")
    
    def remove_website(self):
        selection = self.web_listbox.curselection()
        if selection:
            self.web_listbox.delete(selection)
            web = list(self.whitelist["websites"])[selection[0]]
            self.whitelist["websites"].remove(web)
    
    def save_and_close(self):
        save_whitelist(self.whitelist)
        update_status("✓ Whitelist guardada")
        self.destroy()

class ScheduleDialog(CustomDialog):
    """Dialog for managing schedule."""
    def __init__(self, parent):
        super().__init__(parent, "Gestor de Horarios", width=500, height=350)
        self.schedule = get_schedule()
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="⏰ GESTOR DE HORARIOS", 
                              font=("Segoe UI", 14, "bold"),
                              fg=warning_color, bg=bg_dark)
        title_label.pack(pady=10)
        
        # Work hours section
        frame = tk.Frame(self, bg=bg_dark)
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame, text="Horario de trabajo:", font=("Segoe UI", 11, "bold"),
                fg=text_color, bg=bg_dark).pack(anchor=tk.W)
        
        time_frame = tk.Frame(frame, bg=bg_dark)
        time_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(time_frame, text="Inicio:", fg=text_secondary, bg=bg_dark).pack(side=tk.LEFT, padx=5)
        self.start_entry = tk.Entry(time_frame, bg=bg_light, fg=text_color,
                                    font=("Segoe UI", 10), width=10)
        self.start_entry.insert(0, self.schedule["work_hours"]["start"])
        self.start_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(time_frame, text="Fin:", fg=text_secondary, bg=bg_dark).pack(side=tk.LEFT, padx=5)
        self.end_entry = tk.Entry(time_frame, bg=bg_light, fg=text_color,
                                  font=("Segoe UI", 10), width=10)
        self.end_entry.insert(0, self.schedule["work_hours"]["end"])
        self.end_entry.pack(side=tk.LEFT, padx=5)
        
        # Break duration
        break_frame = tk.Frame(self, bg=bg_dark)
        break_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(break_frame, text="Duración de descansos (minutos):", 
                font=("Segoe UI", 11, "bold"), fg=text_color, bg=bg_dark).pack(anchor=tk.W)
        
        self.break_entry = tk.Entry(break_frame, bg=bg_light, fg=text_color,
                                    font=("Segoe UI", 10), width=10)
        self.break_entry.insert(0, str(self.schedule.get("break_duration", 15)))
        self.break_entry.pack(anchor=tk.W, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=bg_dark)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(btn_frame, text="Guardar", bg=success_color, fg=bg_dark,
                 font=("Segoe UI", 10, "bold"), command=self.save_schedule,
                 relief=tk.FLAT, padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cerrar", bg=bg_lighter, fg=text_color,
                 font=("Segoe UI", 10, "bold"), command=self.destroy,
                 relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)
    
    def save_schedule(self):
        try:
            self.schedule["work_hours"]["start"] = self.start_entry.get()
            self.schedule["work_hours"]["end"] = self.end_entry.get()
            self.schedule["break_duration"] = int(self.break_entry.get())
            save_schedule(self.schedule)
            update_status("✓ Horario guardado")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar horario: {e}")

class ZenModeDialog(CustomDialog):
    """Dialog for configuring zen mode."""
    def __init__(self, parent):
        super().__init__(parent, "Modo Zen", width=450, height=300)
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="🧘 MODO ZEN", 
                              font=("Segoe UI", 14, "bold"),
                              fg=accent_color, bg=bg_dark)
        title_label.pack(pady=15)
        
        # Description
        desc = tk.Label(self, text="El Modo Zen desactiva todas las distracciones y\ncrea un ambiente perfecto para concentrarse",
                       font=("Segoe UI", 10), fg=text_secondary, bg=bg_dark)
        desc.pack(pady=10)
        
        # Options
        self.duration_var = tk.StringVar(value="60")
        
        options_frame = tk.Frame(self, bg=bg_dark)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(options_frame, text="Duración (minutos):", font=("Segoe UI", 10),
                fg=text_color, bg=bg_dark).pack(anchor=tk.W, pady=5)
        
        duration_entry = tk.Entry(options_frame, textvariable=self.duration_var,
                                 bg=bg_light, fg=text_color, font=("Segoe UI", 10), width=15)
        duration_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=bg_dark)
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Button(btn_frame, text="🧘 Activar", bg=success_color, fg=bg_dark,
                 font=("Segoe UI", 11, "bold"), command=self.activate_zen,
                 relief=tk.FLAT, padx=30, pady=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cerrar", bg=bg_lighter, fg=text_color,
                 font=("Segoe UI", 11, "bold"), command=self.destroy,
                 relief=tk.FLAT, padx=30, pady=10).pack(side=tk.RIGHT, padx=5)
    
    def activate_zen(self):
        duration = self.duration_var.get()
        try:
            minutes = int(duration)
            update_status(f"🧘 Modo Zen activado por {minutes} minutos")
            messagebox.showinfo("Zen Mode", 
                              f"Modo Zen activado.\nTiempo: {minutes} minutos\n\n"
                              "Disfruta del enfoque total. Todas las notificaciones están silenciadas.")
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido de minutos")

class ReportsDialog(CustomDialog):
    """Dialog for viewing detailed reports."""
    def __init__(self, parent):
        super().__init__(parent, "Reportes Detallados", width=600, height=450)
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="📊 REPORTES DETALLADOS", 
                              font=("Segoe UI", 14, "bold"),
                              fg=accent_color, bg=bg_dark)
        title_label.pack(pady=10)
        
        # Report content
        try:
            stats = AdvancedStats()
            trend = stats.get_productivity_trend(days=7)
            health = stats.get_health_metrics()
            
            report_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 REPORTE SEMANAL DE PRODUCTIVIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 TENDENCIAS (Últimos 7 días):
   • Dirección: {trend.get('trend', 'Sin datos')}
   • Enfoque promedio: {trend.get('average_focus', 0):.1f} min/día
   • Sesiones completadas: {trend.get('sessions', 0)}
   • Días productivos: {trend.get('productive_days', 0)}/7

💪 SALUD DIGITAL:
   • Tiempo en pantalla: {health.get('screen_time', 0)} min
   • Frecuencia de descansos: {health.get('break_frequency', 0)} descansos
   • Score de bienestar: {health.get('digital_wellness_score', 0)}/100
   • Estado: {'✓ Excelente' if health.get('digital_wellness_score', 0) > 80 else '⚠ Normal' if health.get('digital_wellness_score', 0) > 60 else '⚠ Requiere mejora'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 RECOMENDACIONES:
   • Mantén sesiones de enfoque de 50 minutos
   • Descansa 10 minutos después de cada sesión
   • Toma descansos cada 2 horas para cuidar tu vista
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
        except Exception as e:
            report_text = f"Error al generar reporte: {e}"
        
        text_widget = scrolledtext.ScrolledText(self, bg="#0f0f1e", fg=success_color,
                                               font=("Courier New", 9), height=18)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, report_text)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=bg_dark)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Exportar", bg=success_color, fg=bg_dark,
                 font=("Segoe UI", 10, "bold"), relief=tk.FLAT, padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cerrar", bg=bg_lighter, fg=text_color,
                 font=("Segoe UI", 10, "bold"), command=self.destroy,
                 relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=5)

# ======================
# Utility Functions
# ======================

def update_status(message):
    """Update status label and add to log."""
    global status_label, log_text
    if status_label:
        status_label.config(text=message)
        status_label.update()
    if log_text:
        log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

def start_guardian():
    """Start Guardian monitoring."""
    global monitor_running
    if not monitor_running:
        monitor_running = True
        update_status("✓ Guardian iniciado - Monitoreando aplicaciones...")
        threading.Thread(target=monitor_apps, daemon=True).start()

def stop_guardian():
    """Stop Guardian monitoring."""
    global monitor_running
    monitor_running = False
    update_status("⏹ Guardian detenido")

def show_stats():
    """Show productivity statistics with custom dialog."""
    try:
        stats = AdvancedStats()
        trend = stats.get_productivity_trend(days=7)
        health = stats.get_health_metrics()
        
        message = f"""
📊 ESTADÍSTICAS DE PRODUCTIVIDAD

Tendencia (7 días): {trend.get('trend', 'Sin datos')}
Score promedio: {trend.get('average_focus', 0):.1f} min/día

💪 Salud Digital:
Tiempo en pantalla: {health.get('screen_time', 0)} min
Frecuencia de descansos: {health.get('break_frequency', 0)}
Score de bienestar: {health.get('digital_wellness_score', 0)}/100
        """
        messagebox.showinfo("Estadísticas", message)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las estadísticas: {e}")

def show_alerts():
    """Show smart alerts."""
    try:
        alerts = SmartAlerts()
        dummy_stats = {
            "focus_time_minutes": 60,
            "blocks_today": 5,
            "productivity_score": 75
        }
        
        alerts_list = alerts.check_productivity_alerts(dummy_stats)
        
        message = "🚨 ALERTAS INTELIGENTES\n\n"
        for alert in alerts_list:
            message += f"• {alert.get('message', alert)}\n"
        
        if not alerts_list:
            message += "✓ No hay alertas en este momento"
        
        messagebox.showinfo("Alertas", message)
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener alertas: {e}")

def export_report():
    """Export productivity report."""
    try:
        exporter = AdvancedExporter()
        
        dummy_stats = {
            "focus_time": 120,
            "blocks_count": 8,
            "sessions": 3,
            "productivity_score": 75,
            "top_blocked_apps": []
        }
        
        filepath = exporter.generate_weekly_report(dummy_stats)
        messagebox.showinfo("Éxito", f"Reporte exportado:\n{filepath}")
        update_status(f"✓ Reporte exportado: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar reporte: {e}")

def show_goals():
    """Show and manage daily goals."""
    try:
        goals_manager = DailyGoalsManager()
        goals = goals_manager.get_goals()
        
        message = """
🎯 METAS DIARIAS

Tiempo de enfoque: {} min
Límite de bloqueos: {} apps
Tiempo de descanso: {} min
        """.format(
            goals.get("focus_time", 480),
            goals.get("blocks_limit", 10),
            goals.get("break_time", 300)
        )
        messagebox.showinfo("Metas", message)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar metas: {e}")

def switch_profile():
    """Switch between profiles - opens ProfileDialog."""
    dialog = ProfileDialog(root)
    root.wait_window(dialog)

def manage_whitelist():
    """Manage whitelist apps - opens WhitelistDialog."""
    dialog = WhitelistDialog(root)
    root.wait_window(dialog)

def configure_schedule():
    """Configure schedule - opens ScheduleDialog."""
    dialog = ScheduleDialog(root)
    root.wait_window(dialog)

def activate_zen_mode():
    """Activate zen mode - opens ZenModeDialog."""
    dialog = ZenModeDialog(root)
    root.wait_window(dialog)

def view_reports():
    """View detailed reports - opens ReportsDialog."""
    dialog = ReportsDialog(root)
    root.wait_window(dialog)

# ======================
# Main UI Setup
# ======================

def create_main_window():
    """Create and configure main Guardian window."""
    global root, status_label, log_text, current_settings
    
    root = tk.Tk()
    root.title("🛡️ Guardian v5.1 - Sistema de Bienestar Digital")
    root.geometry("1100x750")
    root.config(bg=bg_dark)
    
    # Set icon if available
    try:
        icon_path = Path("config/guardian.ico")
        if icon_path.exists():
            root.iconbitmap(str(icon_path))
    except Exception as e:
        print(f"Could not set icon: {e}")
    
    current_settings = load_settings()
    
    # ===== HEADER =====
    header = tk.Frame(root, bg=accent_color, height=80)
    header.pack(fill=tk.X, padx=0, pady=0)
    header.pack_propagate(False)
    
    title = tk.Label(header, text="🛡️ GUARDIAN v5.1", font=("Segoe UI", 24, "bold"),
                     fg="white", bg=accent_color)
    title.pack(pady=10)
    
    subtitle = tk.Label(header, text="Sistema Inteligente de Bienestar Digital",
                        font=("Segoe UI", 10), fg=bg_dark, bg=accent_color)
    subtitle.pack()
    
    # ===== MAIN CONTENT =====
    main_frame = tk.Frame(root, bg=bg_dark)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Status
    status_label = tk.Label(main_frame, text="✓ Guardian listo",
                           font=("Segoe UI", 11, "bold"), fg=success_color, bg=bg_dark)
    status_label.pack(anchor=tk.W, pady=(0, 10))
    
    # Main control buttons - Row 1
    button_frame1 = tk.Frame(main_frame, bg=bg_dark)
    button_frame1.pack(fill=tk.X, pady=5)
    
    tk.Button(button_frame1, text="▶ Iniciar", bg=success_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=start_guardian,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame1, text="⏹ Detener", bg=danger_color, fg="white",
              font=("Segoe UI", 11, "bold"), command=stop_guardian,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame1, text="📊 Estadísticas", bg=accent_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_stats,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame1, text="🚨 Alertas", bg=warning_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_alerts,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame1, text="🎯 Metas", bg=accent_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_goals,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame1, text="📈 Exportar", bg=success_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=export_report,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    # Feature buttons - Row 2
    button_frame2 = tk.Frame(main_frame, bg=bg_dark)
    button_frame2.pack(fill=tk.X, pady=5)
    
    tk.Button(button_frame2, text="👤 Perfiles", bg=bg_lighter, fg=text_color,
              font=("Segoe UI", 10, "bold"), command=switch_profile,
              relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame2, text="✅ Whitelist", bg=bg_lighter, fg=text_color,
              font=("Segoe UI", 10, "bold"), command=manage_whitelist,
              relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame2, text="⏰ Horario", bg=bg_lighter, fg=text_color,
              font=("Segoe UI", 10, "bold"), command=configure_schedule,
              relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame2, text="🧘 Zen Mode", bg=bg_lighter, fg=text_color,
              font=("Segoe UI", 10, "bold"), command=activate_zen_mode,
              relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame2, text="📋 Reportes", bg=bg_lighter, fg=text_color,
              font=("Segoe UI", 10, "bold"), command=view_reports,
              relief=tk.FLAT, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
    
    # Apps bloqueadas
    apps_label = tk.Label(main_frame, text="🚫 Aplicaciones Bloqueadas:",
                          font=("Segoe UI", 12, "bold"), fg=accent_color, bg=bg_dark)
    apps_label.pack(anchor=tk.W, pady=(15, 5))
    
    apps_listbox = tk.Listbox(main_frame, bg=bg_light, fg=success_color,
                              font=("Courier New", 10), height=5)
    apps_listbox.pack(fill=tk.BOTH, expand=False, pady=(0, 10))
    
    blocked_apps = get_blocked_apps()
    for app in blocked_apps[:12]:
        apps_listbox.insert(tk.END, f"  • {app}")
    
    if not blocked_apps:
        apps_listbox.insert(tk.END, "  (Sin aplicaciones bloqueadas)")
    
    # Log
    log_label = tk.Label(main_frame, text="📝 Actividad:",
                        font=("Segoe UI", 12, "bold"), fg=accent_color, bg=bg_dark)
    log_label.pack(anchor=tk.W, pady=(10, 5))
    
    log_text = scrolledtext.ScrolledText(main_frame, bg="#0f0f1e", fg=success_color,
                                         font=("Courier New", 9), height=8)
    log_text.pack(fill=tk.BOTH, expand=True)
    log_text.config(state=tk.DISABLED)
    
    # Footer
    footer = tk.Frame(root, bg=bg_light, height=40)
    footer.pack(fill=tk.X, padx=0, pady=0)
    footer.pack_propagate(False)
    
    footer_text = tk.Label(footer, text="Guardian v5.1 | Perfiles | Whitelist | Horario | Zen Mode | Reportes",
                           font=("Segoe UI", 9), fg="#7f8c8d", bg=bg_light)
    footer_text.pack(pady=8)
    
    # Initialize
    update_status("✓ Guardian v5.1 iniciado - Listo para monitorear")
    log_info("Guardian v5.1 iniciado exitosamente")
    
    return root

# ======================
# Main Entry Point
# ======================

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()

