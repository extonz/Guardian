"""
Demo interactiva de todas las nuevas funciones de Guardian.
Ejecutar: python demo_new_features.py
"""

from src.features.enhanced_ui import TimeTracker, FocusTimer, ProgressBar
from src.features.advanced_analytics import (
    ProductivityAnalyzer, BreakReminderSystem, HealthMonitor, InsightGenerator
)
from src.utils.advanced_utilities import (
    ThemeManager, NotificationCenter, AchievementSystem, SessionManager
)
from datetime import datetime
import time


def demo_productivity_analyzer():
    """Demo del analizador de productividad."""
    print("\n" + "="*60)
    print("📊 DEMO: Analizador de Productividad")
    print("="*60)
    
    analyzer = ProductivityAnalyzer()
    
    # Simular un día de trabajo
    print("\n▶ Registrando eventos del día...")
    analyzer.record_block("YouTube", datetime.now())
    analyzer.record_block("TikTok", datetime.now())
    analyzer.record_block("YouTube", datetime.now())
    analyzer.record_focus_session(25, quality=0.9)
    analyzer.record_focus_session(30, quality=0.85)
    
    # Resultados
    stats = analyzer.get_daily_stats()
    print(f"\n✓ Estadísticas del día:")
    print(f"  - Bloques: {stats['blocks_today']}")
    print(f"  - Tiempo de enfoque: {stats['focus_time_minutes']} minutos")
    print(f"  - Sesiones: {stats['sessions_today']}")
    print(f"  - Apps bloqueadas: {stats['unique_apps_blocked']}")
    
    score = analyzer.get_productivity_score()
    print(f"\n📈 Score de productividad: {score}/100")
    
    most_blocked = analyzer.get_most_blocked_app()
    print(f"🚫 App más bloqueada: {most_blocked}")


def demo_focus_timer():
    """Demo del timer Pomodoro."""
    print("\n" + "="*60)
    print("⏱️  DEMO: Timer Pomodoro")
    print("="*60)
    
    timer = FocusTimer(work_minutes=25, break_minutes=5)
    
    print(f"\n▶ Timer iniciado: {timer.get_display_time()}")
    print(f"  Sesión: {'TRABAJO' if not timer.is_break else 'DESCANSO'}")
    
    # Simular algunos ticks
    for i in range(3):
        print(f"  [{timer.get_display_time()}] Contando...")
        timer.current_time -= 60  # Simular 1 minuto
    
    print(f"\n✓ Timer actual: {timer.get_display_time()}")


def demo_break_reminder():
    """Demo del sistema de recordatorio de descansos."""
    print("\n" + "="*60)
    print("☕ DEMO: Sistema de Recordatorios de Descanso")
    print("="*60)
    
    break_sys = BreakReminderSystem(focus_minutes=25)
    
    print("\n▶ Generando sugerencias de descanso...")
    for i in range(3):
        suggestion = break_sys.get_break_suggestion()
        print(f"  {i+1}. {suggestion}")
    
    time_left = break_sys.get_time_until_break()
    print(f"\n⏳ Tiempo hasta el próximo descanso: {time_left} minutos")


def demo_health_monitor():
    """Demo del monitor de salud."""
    print("\n" + "="*60)
    print("❤️  DEMO: Monitor de Salud Digital")
    print("="*60)
    
    health = HealthMonitor()
    
    # Simular un día
    print("\n▶ Simulando un día de uso...")
    health.add_screen_time(120)  # 2 horas
    health.log_break()
    health.log_break()
    
    score = health.get_health_score()
    print(f"\n✓ Score de salud: {score}/100")
    
    recommendations = health.get_health_recommendations()
    if recommendations:
        print(f"\n💡 Recomendaciones:")
        for rec in recommendations:
            print(f"  - {rec}")
    else:
        print(f"\n✓ ¡Excelente salud digital!")


def demo_achievements():
    """Demo del sistema de logros."""
    print("\n" + "="*60)
    print("🏆 DEMO: Sistema de Logros")
    print("="*60)
    
    achievements = AchievementSystem()
    
    print("\n▶ Desbloqueando logros...")
    unlocked = [
        achievements.unlock_achievement('first_block'),
        achievements.unlock_achievement('focus_warrior'),
    ]
    
    for achievement in unlocked:
        if achievement:
            print(f"  ✓ Desbloqueado: {achievement['icon']} {achievement['name']}")
    
    progress = achievements.get_unlock_progress()
    print(f"\n📊 Progreso general:")
    print(f"  - Desbloqueados: {progress['unlocked']}/{progress['total']}")
    print(f"  - Porcentaje: {progress['percentage']:.1f}%")


def demo_session_manager():
    """Demo del gestor de sesiones."""
    print("\n" + "="*60)
    print("📝 DEMO: Gestor de Sesiones")
    print("="*60)
    
    sessions = SessionManager('demo_sessions.json')
    
    print("\n▶ Creando una sesión...")
    session = sessions.start_session("Estudio de Matemáticas", focus_time=30)
    print(f"  Sesión iniciada: {session['name']}")
    
    # Simular trabajo
    print("  [Trabajando...]")
    time.sleep(2)
    
    print("\n▶ Finalizando sesión...")
    completed = sessions.end_session(notes="Cubrí 2 temas importantes")
    
    if completed:
        print(f"  ✓ Sesión completada")
        print(f"    - Nombre: {completed['name']}")
        print(f"    - Notas: {completed['notes']}")


def demo_notification_center():
    """Demo del centro de notificaciones."""
    print("\n" + "="*60)
    print("🔔 DEMO: Centro de Notificaciones")
    print("="*60)
    
    notif_center = NotificationCenter()
    
    print("\n▶ Agregando notificaciones...")
    notif_center.add_notification(
        "Descanso", 
        "Es hora de tomar un descanso",
        notification_type='warning'
    )
    notif_center.add_notification(
        "Logro Desbloqueado",
        "¡Completaste 5 sesiones!",
        notification_type='success'
    )
    
    unread = notif_center.get_unread_count()
    print(f"\n✓ Notificaciones no leídas: {unread}")
    
    notifications = notif_center.get_notifications()
    print(f"\n📋 Últimas notificaciones:")
    for n in notifications[:2]:
        print(f"  - [{n['type']}] {n['title']}: {n['message']}")


def demo_themes():
    """Demo del gestor de temas."""
    print("\n" + "="*60)
    print("🎨 DEMO: Gestor de Temas")
    print("="*60)
    
    print("\n▶ Temas disponibles:")
    for theme in ThemeManager.list_themes():
        print(f"  - {theme}")
    
    print("\n▶ Colores del tema 'dark':")
    dark_theme = ThemeManager.get_theme('dark')
    for color_name, color_value in list(dark_theme.items())[:4]:
        print(f"  - {color_name}: {color_value}")


def demo_insights():
    """Demo del generador de insights."""
    print("\n" + "="*60)
    print("💡 DEMO: Generador de Insights")
    print("="*60)
    
    analyzer = ProductivityAnalyzer()
    
    # Simular datos
    analyzer.record_block("TikTok")
    analyzer.record_block("YouTube")
    analyzer.record_focus_session(120, quality=0.95)
    
    insight_gen = InsightGenerator(analyzer)
    
    print("\n▶ Insights diarios:")
    insights = insight_gen.generate_daily_insights()
    for insight in insights:
        print(f"  - {insight}")
    
    print("\n▶ Recomendaciones:")
    recommendations = insight_gen.generate_recommendations()
    for rec in recommendations:
        print(f"  - {rec}")


def main():
    """Ejecuta todos los demos."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "🛡️  GUARDIAN - DEMO DE NUEVAS FUNCIONES".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    demos = [
        ("Analizador de Productividad", demo_productivity_analyzer),
        ("Timer Pomodoro", demo_focus_timer),
        ("Sistema de Descansos", demo_break_reminder),
        ("Monitor de Salud", demo_health_monitor),
        ("Sistema de Logros", demo_achievements),
        ("Gestor de Sesiones", demo_session_manager),
        ("Centro de Notificaciones", demo_notification_center),
        ("Gestor de Temas", demo_themes),
        ("Generador de Insights", demo_insights),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error en demo: {e}")
    
    print("\n" + "="*60)
    print("✅ Demo completado!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
