#!/usr/bin/env python3
"""
Guardian - Sistema de Bienestar Digital v5.1
App principal mejorada y simplificada
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime

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

# Colors
bg_dark = "#0a0e27"
bg_light = "#1a1f3a"
accent_color = "#00d4ff"
success_color = "#00ff88"
warning_color = "#ffaa00"
danger_color = "#ff3333"

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
    """Show productivity statistics."""
    try:
        stats = AdvancedStats()
        trend = stats.get_productivity_trend(days=7)
        health = stats.get_health_metrics()
        
        message = f"""
📊 ESTADÍSTICAS DE PRODUCTIVIDAD

Tendencia (7 días): {trend['trend']}
Score promedio: {trend['average_focus']:.1f} min/día

💪 Salud Digital:
Tiempo en pantalla: {health['screen_time']} min
Frecuencia de descansos: {health['break_frequency']}
Score de bienestar: {health['digital_wellness_score']}/100
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
            message += f"• {alert['message']}\n"
        
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
            goals["focus_time"],
            goals["blocks_limit"],
            goals["break_time"]
        )
        messagebox.showinfo("Metas", message)
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar metas: {e}")

# ======================
# Main UI Setup
# ======================

def create_main_window():
    """Create and configure main Guardian window."""
    global root, status_label, log_text, current_settings
    
    root = tk.Tk()
    root.title("🛡️ Guardian v5.1 - Sistema de Bienestar Digital")
    root.geometry("1000x700")
    root.config(bg=bg_dark)
    
    current_settings = load_settings()
    
    # ===== HEADER =====
    header = tk.Frame(root, bg=accent_color, height=80)
    header.pack(fill=tk.X, padx=0, pady=0)
    header.pack_propagate(False)
    
    title = tk.Label(header, text="🛡️ GUARDIAN v5.1", font=("Segoe UI", 24, "bold"),
                     fg="white", bg=accent_color)
    title.pack(pady=15)
    
    subtitle = tk.Label(header, text="Sistema Inteligente de Bienestar Digital",
                        font=("Segoe UI", 10), fg=bg_dark, bg=accent_color)
    subtitle.pack()
    
    # ===== MAIN CONTENT =====
    main_frame = tk.Frame(root, bg=bg_dark)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Status
    status_label = tk.Label(main_frame, text="✓ Guardian listo",
                           font=("Segoe UI", 11), fg=success_color, bg=bg_dark)
    status_label.pack(anchor=tk.W, pady=(0, 10))
    
    # Control buttons
    button_frame = tk.Frame(main_frame, bg=bg_dark)
    button_frame.pack(fill=tk.X, pady=10)
    
    tk.Button(button_frame, text="▶ Iniciar", bg=success_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=start_guardian,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="⏹ Detener", bg=danger_color, fg="white",
              font=("Segoe UI", 11, "bold"), command=stop_guardian,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="📊 Estadísticas", bg=accent_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_stats,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="🚨 Alertas", bg=warning_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_alerts,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="🎯 Metas", bg=accent_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=show_goals,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="📈 Exportar", bg=success_color, fg=bg_dark,
              font=("Segoe UI", 11, "bold"), command=export_report,
              relief=tk.FLAT, padx=20, pady=10).pack(side=tk.LEFT, padx=5)
    
    # Apps bloqueadas
    apps_label = tk.Label(main_frame, text="🚫 Aplicaciones Bloqueadas:",
                          font=("Segoe UI", 12, "bold"), fg=accent_color, bg=bg_dark)
    apps_label.pack(anchor=tk.W, pady=(10, 5))
    
    apps_listbox = tk.Listbox(main_frame, bg=bg_light, fg=success_color,
                              font=("Courier New", 10), height=6)
    apps_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    blocked_apps = get_blocked_apps()
    for app in blocked_apps[:15]:
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
    
    footer_text = tk.Label(footer, text="Guardian v5.1 | Metas Diarias | Estadísticas | Alertas Inteligentes | Exportación",
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
    try:
        root = create_main_window()
        root.mainloop()
    except Exception as e:
        print(f"Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

