import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, filedialog
from src.monitor import monitor_apps
from src.settings_manager import load_settings, save_settings, get_blocked_apps, get_session_stats
from src.logger import log_info

# Try importing optional modules
try:
    from src.reports import get_daily_stats, get_weekly_stats, get_progress_percentage
except ImportError:
    pass

try:
    from src.gamification import get_gamification_status, update_streak, check_and_unlock_badges
except ImportError:
    pass

try:
    from src.security import is_vpn_active, detect_second_monitor, is_virtual_machine
except ImportError:
    pass

try:
    from src.zen_mode import start_zen_mode
except ImportError:
    pass

# New functionality imports (v5.1)
try:
    from src.daily_goals import DailyGoalsManager
    from src.advanced_stats import AdvancedStats
    from src.smart_alerts import SmartAlerts
    from src.session_tracker import SessionTracker
    from src.advanced_exporter import AdvancedExporter
except ImportError as e:
    print(f"Warning: Some new modules not available: {e}")

# Variables globales para la UI
status_label = None
log_text = None
monitor_running = False
stats_label = None
current_settings = load_settings()

def update_status(message):
    """Actualiza el mensaje de estado en la UI y agrega al log"""
    global status_label, log_text
    if status_label:
        status_label.config(text=message)
        status_label.update()
    if log_text:
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)

def update_stats():
    """Actualiza las estadísticas mostradas."""
    global stats_label
    if stats_label:
        stats = get_session_stats()
        gamif = get_gamification_status()
        
        stats_text = f"Bloques hoy: {stats['total_blocks_today']} | "
        stats_text += f"Puntos: {gamif['points']} | "
        stats_text += f"Nivel: {gamif['level']} | "
        stats_text += f"Streak: {gamif['streak']} días"
        stats_label.config(text=stats_text)

def start_monitor():
    global monitor_running
    if not monitor_running:
        monitor_running = True
        log_info("Guardian iniciado")
        btn_start.config(state=tk.DISABLED, bg="#95a5a6")
        btn_stop.config(state=tk.NORMAL, bg="#e74c3c")
        t = threading.Thread(target=monitor_loop, daemon=True)
        t.start()
        update_status("✓ Guardian iniciado - Monitoreando apps...")

def monitor_loop():
    """Loop del monitor que actualiza estadísticas."""
    while monitor_running:
        monitor_apps(update_status)
        update_stats()
        threading.Event().wait(1)

def stop_monitor():
    global monitor_running
    monitor_running = False
    btn_start.config(state=tk.NORMAL, bg="#27ae60")
    btn_stop.config(state=tk.DISABLED, bg="#95a5a6")
    log_info("Guardian detenido")
    update_status("✗ Guardian detenido")

def open_config_panel():
    """Abre el panel de configuración."""
    config_window = tk.Toplevel(root)
    config_window.title("Configuración de Guardian")
    config_window.geometry("700x900")
    config_window.resizable(True, True)
    config_window.config(bg=bg_dark)
    
    # Header
    header = tk.Frame(config_window, bg=accent_color)
    header.pack(fill=tk.X, padx=0, pady=0)
    tk.Label(header, text="⚙️ CONFIGURACIÓN", font=("Segoe UI", 16, "bold"), 
             fg="white", bg=accent_color, pady=15).pack()
    
    main = tk.Frame(config_window, bg=bg_dark)
    main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Scroll
    canvas = tk.Canvas(main, bg=bg_dark, highlightthickness=0)
    scrollbar = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_dark)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # ===== PERFILES =====
    profile_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    profile_frame.pack(fill=tk.X, pady=10, padx=10)
    tk.Label(profile_frame, text="📋 Perfil Actual:", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    profiles = get_profiles()
    profile_var = tk.StringVar(value=current_settings['current_profile'])
    
    profile_menu = tk.OptionMenu(profile_frame, profile_var, *profiles.keys(),
                                command=lambda p: switch_profile(p))
    profile_menu.pack(anchor=tk.W, padx=10, pady=(5,10), fill=tk.X)
    
    # ===== HORARIOS =====
    schedule_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    schedule_frame.pack(fill=tk.X, pady=10, padx=10)
    tk.Label(schedule_frame, text="⏰ Horarios de Bloqueo:", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    def config_schedule():
        hour_start = simpledialog.askinteger("Horario", "Hora inicio (0-23):", minvalue=0, maxvalue=23)
        if hour_start is not None:
            hour_end = simpledialog.askinteger("Horario", "Hora fin (0-23):", minvalue=0, maxvalue=23)
            if hour_end is not None:
                set_schedule(current_settings['current_profile'], 'monday', hour_start, hour_end)
                messagebox.showinfo("Éxito", f"Horario configurado: {hour_start}:00 - {hour_end}:00")
    
    tk.Button(schedule_frame, text="⏰ Configurar Horario", bg=accent_color, fg="white",
              command=config_schedule, relief=tk.FLAT).pack(padx=10, pady=10, fill=tk.X)
    
    # ===== DETECCIÓN DE EVASIÓN =====
    detection_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    detection_frame.pack(fill=tk.X, pady=10, padx=10)
    tk.Label(detection_frame, text="🔍 Detección de Evasión:", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    def check_evasion():
        vpn = is_vpn_active()
        monitor = detect_second_monitor()
        vm = is_virtual_machine()
        
        info = f"VPN Activa: {'✓ Sí' if vpn else '✗ No'}\n"
        info += f"Segundo Monitor: {'✓ Sí' if monitor else '✗ No'}\n"
        info += f"Máquina Virtual: {'✓ Sí' if vm else '✗ No'}"
        messagebox.showinfo("Estado de Seguridad", info)
    
    tk.Button(detection_frame, text="🔍 Verificar Seguridad", bg=success_color, fg="white",
              command=check_evasion, relief=tk.FLAT).pack(padx=10, pady=10, fill=tk.X)
    
    # ===== APPS BLOQUEADAS =====
    apps_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    apps_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
    tk.Label(apps_frame, text="🚫 Apps Bloqueadas:", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    apps_listbox = tk.Listbox(apps_frame, bg="#0f0f1e", fg="#00ff00", 
                              font=("Consolas", 9), height=8)
    apps_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    blocked_apps = get_blocked_apps()
    for app in blocked_apps:
        apps_listbox.insert(tk.END, app)
    
    def add_app():
        app = simpledialog.askstring("Agregar App", "Nombre de la aplicación:")
        if app:
            add_blocked_app(app)
            apps_listbox.insert(tk.END, app)
            update_status(f"✓ {app} agregada a la lista de bloqueo")
    
    def remove_app():
        try:
            idx = apps_listbox.curselection()[0]
            app = apps_listbox.get(idx)
            remove_blocked_app(app)
            apps_listbox.delete(idx)
            update_status(f"✓ {app} removida de la lista de bloqueo")
        except:
            messagebox.showwarning("Error", "Selecciona una app para remover")
    
    btn_frame = tk.Frame(apps_frame, bg=bg_light)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(btn_frame, text="➕ Agregar", bg=success_color, fg="white",
              command=add_app, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="➖ Remover", bg=danger_color, fg="white",
              command=remove_app, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="📥 Importar CSV", bg=accent_color, fg="white",
              command=lambda: import_csv_dialog(), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="📤 Exportar CSV", bg="#9b59b6", fg="white",
              command=lambda: show_message(*export_apps_csv()), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    
    # ===== WHITELIST =====
    whitelist_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    whitelist_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
    tk.Label(whitelist_frame, text="✅ Whitelist (Excepciones):", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    whitelist_listbox = tk.Listbox(whitelist_frame, bg="#0f0f1e", fg="#00ff00",
                                   font=("Consolas", 9), height=5)
    whitelist_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    whitelist = get_whitelist()
    for app in whitelist:
        whitelist_listbox.insert(tk.END, app)
    
    def add_whitelist():
        app = simpledialog.askstring("Agregar Excepción", "Nombre de la aplicación:")
        if app:
            add_to_whitelist(app)
            whitelist_listbox.insert(tk.END, app)
            update_status(f"✓ {app} agregada a whitelist")
    
    whitelist_btn_frame = tk.Frame(whitelist_frame, bg=bg_light)
    whitelist_btn_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(whitelist_btn_frame, text="➕ Agregar Excepción", bg="#9b59b6", fg="white",
              command=add_whitelist, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    
    # ===== BACKUP =====
    backup_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    backup_frame.pack(fill=tk.X, pady=10, padx=10)
    tk.Label(backup_frame, text="💾 Backup y Restauración:", font=("Segoe UI", 11, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    backup_btn = tk.Frame(backup_frame, bg=bg_light)
    backup_btn.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(backup_btn, text="💾 Crear Backup", bg=success_color, fg="white",
              command=lambda: show_message(*export_settings_backup()), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(backup_btn, text="📂 Restaurar Backup", bg=accent_color, fg="white",
              command=lambda: restore_backup_dialog(), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

def import_csv_dialog():
    """Diálogo para importar CSV."""
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        success, msg = import_apps_csv(file)
        show_message(success, msg)

def restore_backup_dialog():
    """Diálogo para restaurar backup."""
    file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file:
        success, msg = import_settings_backup(file)
        show_message(success, msg)

def show_message(success, msg):
    """Muestra mensaje de éxito o error."""
    if success:
        messagebox.showinfo("Éxito", msg)
    else:
        messagebox.showerror("Error", msg)

def open_advanced_panel():
    """Panel avanzado con gamificación, análisis, bloqueo de sitios, etc."""
    adv_window = tk.Toplevel(root)
    adv_window.title("Panel Avanzado Guardian")
    adv_window.geometry("850x750")
    adv_window.config(bg=bg_dark)
    
    # Header
    header = tk.Frame(adv_window, bg=accent_color)
    header.pack(fill=tk.X, padx=0, pady=0)
    tk.Label(header, text="🚀 PANEL AVANZADO", font=("Segoe UI", 16, "bold"), 
             fg="white", bg=accent_color, pady=15).pack()
    
    # Tabs
    canvas = tk.Canvas(adv_window, bg=bg_dark, highlightthickness=0)
    scrollbar = tk.Scrollbar(adv_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_dark)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # ===== GAMIFICACIÓN =====
    gamif_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    gamif_frame.pack(fill=tk.X, pady=10, padx=10)
    
    tk.Label(gamif_frame, text="🎮 GAMIFICACIÓN", font=("Segoe UI", 12, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    def show_gamification():
        gamif = get_gamification_status()
        info = f"""
📊 TU PROGRESO:
├─ Puntos: {gamif['points']}
├─ Nivel: {gamif['level']}
├─ Streak: {gamif['streak']} días
├─ Horas de enfoque: {gamif['hours']}
├─ Progreso al siguiente nivel: {gamif['progress_to_next_level']:.0f}%
└─ Badges desbloqueadas: {len(gamif['badges'])}

🏅 TUS LOGROS:
{chr(10).join(['  • ' + b for b in gamif['badges']])}
        """
        messagebox.showinfo("Gamificación", info)
    
    tk.Button(gamif_frame, text="🎮 Ver Progreso", bg=success_color, fg="white",
              command=show_gamification, relief=tk.FLAT).pack(padx=10, pady=10, fill=tk.X)
    
    # ===== ANÁLISIS INTELIGENTE =====
    ml_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    ml_frame.pack(fill=tk.X, pady=10, padx=10)
    
    tk.Label(ml_frame, text="🤖 ANÁLISIS INTELIGENTE", font=("Segoe UI", 12, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    def show_analysis():
        risk, score = predict_distraction_risk()
        best = get_best_focus_times()
        worst = get_worst_focus_times()
        suggestions = suggest_strategy()
        
        info = f"""
⚡ RIESGO ACTUAL:
├─ Nivel: {risk.upper()}
└─ Score: {score}/100

✅ MEJORES HORARIOS:
{' '.join([f'{h:02d}:00' for h in sorted(best)]) if best else 'Sin datos'}

❌ HORARIOS PELIGROSOS:
{' '.join([f'{h:02d}:00' for h in sorted(worst)]) if worst else 'Sin datos'}

💡 RECOMENDACIONES:
{chr(10).join(suggestions)}
        """
        messagebox.showinfo("Análisis Inteligente", info)
    
    tk.Button(ml_frame, text="🤖 Analizar Patrones", bg="#3498db", fg="white",
              command=show_analysis, relief=tk.FLAT).pack(padx=10, pady=10, fill=tk.X)
    
    # ===== BLOQUEO DE SITIOS WEB =====
    web_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    web_frame.pack(fill=tk.X, pady=10, padx=10)
    
    tk.Label(web_frame, text="🌐 BLOQUEAR SITIOS WEB", font=("Segoe UI", 12, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    # Lista de sitios bloqueados
    blocked_sites_listbox = tk.Listbox(web_frame, bg="#0f0f1e", fg="#00ff00",
                                       font=("Consolas", 9), height=5)
    blocked_sites_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def refresh_blocked_sites():
        blocked_sites_listbox.delete(0, tk.END)
        for site in get_blocked_sites():
            blocked_sites_listbox.insert(tk.END, site)
    
    def add_blocked_site():
        domain = simpledialog.askstring("Bloquear Sitio", "Dominio (ej: facebook.com):")
        if domain:
            success, msg = block_site(domain)
            if success:
                refresh_blocked_sites()
            show_message(success, msg)
    
    def remove_blocked_site():
        try:
            idx = blocked_sites_listbox.curselection()[0]
            domain = blocked_sites_listbox.get(idx)
            success, msg = unblock_site(domain)
            if success:
                refresh_blocked_sites()
            show_message(success, msg)
        except:
            messagebox.showwarning("Error", "Selecciona un sitio")
    
    refresh_blocked_sites()
    
    web_btn = tk.Frame(web_frame, bg=bg_light)
    web_btn.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(web_btn, text="➕ Bloquear Sitio", bg=danger_color, fg="white",
              command=add_blocked_site, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(web_btn, text="➖ Desbloquear", bg=success_color, fg="white",
              command=remove_blocked_site, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    
    # ===== INTEGRACIÓN NOTIFICACIONES =====
    notif_frame = tk.Frame(scrollable_frame, bg=bg_light, relief=tk.RAISED, bd=2)
    notif_frame.pack(fill=tk.X, pady=10, padx=10)
    
    tk.Label(notif_frame, text="📢 NOTIFICACIONES", font=("Segoe UI", 12, "bold"),
             fg=accent_color, bg=bg_light).pack(anchor=tk.W, padx=10, pady=(10,5))
    
    def setup_telegram_dialog():
        token = simpledialog.askstring("Telegram", "Bot Token:")
        if token:
            chat_id = simpledialog.askstring("Telegram", "Chat ID:")
            if chat_id:
                from src.integrations.notifications import setup_telegram
                setup_telegram(token, chat_id)
                messagebox.showinfo("Éxito", "Telegram configurado")
    
    def setup_discord_dialog():
        webhook = simpledialog.askstring("Discord", "Webhook URL:")
        if webhook:
            from src.integrations.notifications import setup_discord
            setup_discord(webhook)
            messagebox.showinfo("Éxito", "Discord configurado")
    
    notif_btn = tk.Frame(notif_frame, bg=bg_light)
    notif_btn.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(notif_btn, text="📱 Telegram", bg="#0088cc", fg="white",
              command=setup_telegram_dialog, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    tk.Button(notif_btn, text="💬 Discord", bg="#5865f2", fg="white",
              command=setup_discord_dialog, relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

def open_logs_panel():
    """Abre el panel de logs detallados."""
    logs_window = tk.Toplevel(root)
    logs_window.title("Historial Detallado y Reportes")
    logs_window.geometry("800x700")
    logs_window.config(bg=bg_dark)
    
    # Header
    header = tk.Frame(logs_window, bg=accent_color)
    header.pack(fill=tk.X, padx=0, pady=0)
    tk.Label(header, text="📊 HISTORIAL Y REPORTES", font=("Segoe UI", 16, "bold"),
             fg="white", bg=accent_color, pady=15).pack()
    
    # Tabs simulados con botones
    tab_frame = tk.Frame(logs_window, bg=bg_light)
    tab_frame.pack(fill=tk.X, padx=15, pady=10)
    
    text_display = scrolledtext.ScrolledText(logs_window, bg="#0f0f1e", fg="#00ff00",
                                            font=("Consolas", 9), relief=tk.FLAT)
    text_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
    
    def show_logs():
        from src.utils.logger import read_logs
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        logs = read_logs(days=7)
        text_display.insert(tk.END, "".join(logs))
        text_display.config(state=tk.DISABLED)
    
    def show_daily_stats():
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        stats = get_daily_stats()
        text = f"📊 ESTADÍSTICAS HOY ({stats['date']})\n"
        text += f"{'='*50}\n\n"
        text += f"Total de bloques: {stats['total_blocks']}\n"
        text += f"Horas activas: {stats['hours_active']}\n"
        text += f"App más bloqueada: {stats['most_blocked']}\n\n"
        text += "Apps bloqueadas:\n"
        for app, count in sorted(stats['apps_blocked'].items(), key=lambda x: x[1], reverse=True):
            text += f"  • {app}: {count} veces\n"
        text_display.insert(tk.END, text)
        text_display.config(state=tk.DISABLED)
    
    def show_weekly_stats():
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        stats = get_weekly_stats()
        text = f"📈 ESTADÍSTICAS SEMANALES\n"
        text += f"{'='*50}\n\n"
        total = sum(s['total_blocks'] for s in stats)
        text += f"Total de bloques esta semana: {total}\n"
        text += f"Progreso: {get_progress_percentage():.1f}% mejor que la semana pasada\n\n"
        
        for stat in stats:
            text += f"{stat['date']}: {stat['total_blocks']} bloques | App principal: {stat['most_blocked']}\n"
        
        text_display.insert(tk.END, text)
        text_display.config(state=tk.DISABLED)
    
    def export_csv():
        success, msg = generate_csv_report('report.csv')
        show_message(success, msg if success else msg)
    
    def export_pdf():
        success, msg = generate_pdf_report('report.pdf')
        show_message(success, msg if success else msg)
    
    tk.Button(tab_frame, text="📝 Logs", bg=accent_color, fg="white",
              command=show_logs, relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
    tk.Button(tab_frame, text="📊 Hoy", bg=success_color, fg="white",
              command=show_daily_stats, relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
    tk.Button(tab_frame, text="📈 Semana", bg="#9b59b6", fg="white",
              command=show_weekly_stats, relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
    tk.Button(tab_frame, text="📥 Exportar CSV", bg="#27ae60", fg="white",
              command=export_csv, relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
    tk.Button(tab_frame, text="📄 Exportar PDF", bg="#e67e22", fg="white",
              command=export_pdf, relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
    
    show_logs()

# Configurar ventana principal
root = tk.Tk()
root.title("Guardian")
root.geometry("800x700")
root.resizable(True, True)


# Colores
bg_dark = "#1e1e2e"
bg_light = "#2d2d44"
accent_color = "#3498db"
text_color = "#ecf0f1"
danger_color = "#e74c3c"
success_color = "#27ae60"

root.config(bg=bg_dark)

# Encabezado
header_frame = tk.Frame(root, bg=accent_color)
header_frame.pack(fill=tk.X, padx=0, pady=0)

title_label = tk.Label(header_frame, text="🛡️ GUARDIAN", 
                       font=("Segoe UI", 24, "bold"), fg="white", bg=accent_color, pady=20)
title_label.pack()

# Frame principal
main_frame = tk.Frame(root, bg=bg_dark)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Estadísticas
stats_frame = tk.Frame(main_frame, bg=bg_light, relief=tk.RAISED, bd=2)
stats_frame.pack(fill=tk.X, pady=(0, 15))

stats_label = tk.Label(stats_frame, text="Bloques hoy: 0", 
                      font=("Segoe UI", 10), fg=accent_color, bg=bg_light)
stats_label.pack(anchor=tk.W, padx=15, pady=10)

# Estado
status_frame = tk.Frame(main_frame, bg=bg_light, relief=tk.RAISED, bd=2)
status_frame.pack(fill=tk.X, pady=(0, 15))

status_title = tk.Label(status_frame, text="Estado Actual:", font=("Segoe UI", 12, "bold"), 
                        fg=accent_color, bg=bg_light, justify=tk.LEFT)
status_title.pack(anchor=tk.W, padx=15, pady=(10, 5))

status_label = tk.Label(status_frame, text="Presiona 'Iniciar Guardian' para comenzar", 
                       font=("Segoe UI", 11), fg=text_color, bg=bg_light, justify=tk.LEFT, 
                       wraplength=700)
status_label.pack(anchor=tk.W, padx=15, pady=(5, 10))

# Log
log_frame = tk.Frame(main_frame, bg=bg_light, relief=tk.RAISED, bd=2)
log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

log_title = tk.Label(log_frame, text="Historial de Eventos:", font=("Segoe UI", 12, "bold"), 
                     fg=accent_color, bg=bg_light)
log_title.pack(anchor=tk.W, padx=15, pady=(10, 5))

log_text = scrolledtext.ScrolledText(log_frame, height=10, bg="#0f0f1e", fg="#00ff00", 
                                     font=("Consolas", 10), insertbackground="#00ff00",
                                     relief=tk.FLAT, padx=10, pady=10)
log_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))
log_text.config(state=tk.DISABLED)

# Botones
button_frame = tk.Frame(main_frame, bg=bg_dark)
button_frame.pack(fill=tk.X, pady=10)

btn_start = tk.Button(button_frame, text="▶ Iniciar Guardian", font=("Segoe UI", 11, "bold"),
                      fg="white", bg=success_color, activebackground="#229954", 
                      command=start_monitor, relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
btn_start.pack(side=tk.LEFT, padx=5)

btn_stop = tk.Button(button_frame, text="⏹ Detener", font=("Segoe UI", 11, "bold"),
                     fg="white", bg="#95a5a6", activebackground="#7f8c8d", 
                     command=stop_monitor, relief=tk.FLAT, padx=15, pady=8, 
                     cursor="hand2", state=tk.DISABLED)
btn_stop.pack(side=tk.LEFT, padx=5)

btn_config = tk.Button(button_frame, text="⚙️ Configuración", font=("Segoe UI", 11, "bold"),
                       fg="white", bg=accent_color, activebackground="#2980b9", 
                       command=open_config_panel, relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
btn_config.pack(side=tk.LEFT, padx=5)

btn_logs = tk.Button(button_frame, text="📊 Historial", font=("Segoe UI", 11, "bold"),
                     fg="white", bg="#9b59b6", activebackground="#8e44ad", 
                     command=open_logs_panel, relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
btn_logs.pack(side=tk.LEFT, padx=5)

btn_zen = tk.Button(button_frame, text="🧘 Modo Zen", font=("Segoe UI", 11, "bold"),
                    fg="white", bg="#16a085", activebackground="#138d75", 
                    command=lambda: start_zen_mode(int(simpledialog.askinteger("Modo Zen", "Minutos:", minvalue=1, maxvalue=480) or 60)), 
                    relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
btn_zen.pack(side=tk.LEFT, padx=5)

btn_advanced = tk.Button(button_frame, text="🚀 Avanzado", font=("Segoe UI", 11, "bold"),
                         fg="white", bg="#c0392b", activebackground="#a93226", 
                         command=open_advanced_panel, relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
btn_advanced.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="🗑️ Limpiar Log", font=("Segoe UI", 11, "bold"),
                      fg="white", bg="#e67e22", activebackground="#d35400", 
                      relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                      command=lambda: (log_text.config(state=tk.NORMAL), 
                                      log_text.delete(1.0, tk.END), 
                                      log_text.config(state=tk.DISABLED)))
btn_clear.pack(side=tk.RIGHT, padx=5)

# Footer
footer_label = tk.Label(root, text="Guardian v4.0 - Gamificación | IA | Bloqueo Web | Modo Zen | Notificaciones | API REST", 
                       font=("Segoe UI", 9), fg="#7f8c8d", bg=bg_dark)
footer_label.pack(pady=10)

log_info("Guardian v5.1 iniciado")
update_status("👋 Bienvenido a Guardian v5.1. Presiona 'Iniciar Guardian' para comenzar.")

# Guardar dashboard HTML (comentado - función opcional)
# save_dashboard()
update_status("Se ha guardado el dashboard en localhost:8000/dashboard o/y dashboard.html")

# Iniciar API REST en background
try:
#     start_api(port=5000)
except Exception as e:
    print(f"Error iniciando API: {e}")

root.mainloop()

