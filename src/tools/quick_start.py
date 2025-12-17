#!/usr/bin/env python3
"""
🛡️ GUARDIAN - Inicio Rápido de Nuevas Funciones
Script para explorar todas las nuevas funciones agregadas
"""


import os
import sys
import subprocess
from pathlib import Path

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_menu():
    """Muestra el menú principal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"""
{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}║{Colors.ENDC}  🛡️  {Colors.GREEN}GUARDIAN - NUEVAS FUNCIONES{Colors.ENDC}        
{Colors.CYAN}{Colors.BOLD}║{Colors.ENDC}                                                                  
{Colors.CYAN}{Colors.BOLD}║{Colors.ENDC}  9 nuevas funciones + Interfaz rediseñada                      
{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.BOLD}📊 MENÚ PRINCIPAL:{Colors.ENDC}

{Colors.GREEN}1.{Colors.ENDC} {Colors.BOLD}🎨 Abrir Nueva UI Moderna{Colors.ENDC}
   Interfaz completa con dashboard, timer, health monitor e insights
   → Comando: python ui/modern_ui.py

{Colors.GREEN}2.{Colors.ENDC} {Colors.BOLD}🎬 Ver Demostración Interactiva{Colors.ENDC}
   Demuestra todas las nuevas funciones en la terminal
   → Comando: python demo_new_features.py

{Colors.GREEN}3.{Colors.ENDC} {Colors.BOLD}📖 Ver Documentación Completa{Colors.ENDC}
   Abre la documentación de nuevas funciones

{Colors.GREEN}4.{Colors.ENDC} {Colors.BOLD}💻 Ver Código de Componentes{Colors.ENDC}
   Explora los archivos con las nuevas funciones

{Colors.GREEN}5.{Colors.ENDC} {Colors.BOLD}⚙️  Configuración Avanzada{Colors.ENDC}
   Opciones para personalizar Guardian

{Colors.GREEN}6.{Colors.ENDC} {Colors.BOLD}ℹ️  Información y Resumen{Colors.ENDC}
   Detalles completos de cambios

{Colors.RED}0.{Colors.ENDC} {Colors.BOLD}Salir{Colors.ENDC}

{Colors.YELLOW}Selecciona una opción (0-6):{Colors.ENDC} """)

def show_info():
    """Muestra información detallada."""
    print(f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}📋 INFORMACIÓN GENERAL{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}

{Colors.GREEN}✅ CAMBIOS REALIZADOS:{Colors.ENDC}

1. {Colors.BOLD}UI COMPLETAMENTE REDISEÑADA{Colors.ENDC}
   - Dashboard profesional con 5 pestañas
   - Componentes visuales modernos
   - Diseño con gradientes
   - Ejecutar: python ui/modern_ui.py

2. {Colors.BOLD}ANÁLISIS AVANZADO{Colors.ENDC}
   - Análisis automático de productividad
   - Monitor de salud digital
   - Generador de insights personalizados

3. {Colors.BOLD}SISTEMA DE LOGROS{Colors.ENDC}
   - 6 logros desbloqueables
   - Tracking automático
   - Motivación visual

4. {Colors.BOLD}GESTOR DE SESIONES{Colors.ENDC}
   - Crear/finalizar sesiones
   - Persistencia en JSON
   - Análisis de duración

5. {Colors.BOLD}NOTIFICACIONES INTELIGENTES{Colors.ENDC}
   - Centro de notificaciones
   - Badges automáticos
   - Recordatorios de descanso

6. {Colors.BOLD}TEMAS PERSONALIZABLES{Colors.ENDC}
   - Dark, Light, Ocean
   - Fácil de extender
   - Colores consistentes

7. {Colors.BOLD}TIMER POMODORO AVANZADO{Colors.ENDC}
   - Configurable
   - Alternancia automática
   - Display en tiempo real

8. {Colors.BOLD}RESPALDO Y REPORTES{Colors.ENDC}
   - Copias de seguridad
   - Generador de reportes
   - Exportar a JSON

9. {Colors.BOLD}COMPONENTES REUTILIZABLES{Colors.ENDC}
   - ModernButton, StatCard
   - ProgressBar, TimeTracker
   - NotificationBadge

{Colors.YELLOW}📁 ARCHIVOS NUEVOS:{Colors.ENDC}
   • src/features/enhanced_ui.py (374 líneas)
   • src/features/advanced_analytics.py (283 líneas)
   • src/utils/advanced_utilities.py (387 líneas)
   • ui/modern_ui.py (405 líneas)
   • demo_new_features.py (308 líneas)
   • NUEVAS_FUNCIONES.md (documentación)
   • CAMBIOS_NUEVOS.md (guía de uso)

{Colors.YELLOW}📊 ESTADÍSTICAS:{Colors.ENDC}
   • Total líneas agregadas: +1,757
   • Nuevas funciones: 9
   • Componentes UI: 7
   • Archivos nuevos: 7

{Colors.GREEN}🎯 PRÓXIMOS PASOS:{Colors.ENDC}
   1. Ejecutar: python ui/modern_ui.py
   2. Explorar el demo: python demo_new_features.py
   3. Personalizar colores y temas
   4. Integrar en tu flujo de trabajo

Presiona ENTER para volver al menú...
""")
    input()

def show_components():
    """Muestra información sobre los componentes."""
    print(f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}🧩 COMPONENTES DISPONIBLES{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}

{Colors.GREEN}UI COMPONENTS (enhanced_ui.py):{Colors.ENDC}

  • {Colors.BOLD}ModernButton{Colors.ENDC}
    Botones con esquinas redondeadas y hover effect
    
  • {Colors.BOLD}StatCard{Colors.ENDC}
    Tarjetas de estadísticas elegantes
    
  • {Colors.BOLD}ModernTabbedUI{Colors.ENDC}
    Sistema de pestañas moderno
    
  • {Colors.BOLD}ProgressBar{Colors.ENDC}
    Barra de progreso redondeada
    
  • {Colors.BOLD}TimeTracker{Colors.ENDC}
    Rastreador de sesiones
    
  • {Colors.BOLD}FocusTimer{Colors.ENDC}
    Timer Pomodoro configurable
    
  • {Colors.BOLD}NotificationBadge{Colors.ENDC}
    Badge de notificaciones

{Colors.GREEN}ANALYTICS (advanced_analytics.py):{Colors.ENDC}

  • {Colors.BOLD}ProductivityAnalyzer{Colors.ENDC}
    Análisis automático de productividad
    
  • {Colors.BOLD}BreakReminderSystem{Colors.ENDC}
    Recordatorios inteligentes de descanso
    
  • {Colors.BOLD}HealthMonitor{Colors.ENDC}
    Monitor de salud digital
    
  • {Colors.BOLD}InsightGenerator{Colors.ENDC}
    Generador de insights personalizados

{Colors.GREEN}UTILITIES (advanced_utilities.py):{Colors.ENDC}

  • {Colors.BOLD}ThemeManager{Colors.ENDC}
    Gestor de 3 temas predefinidos
    
  • {Colors.BOLD}NotificationCenter{Colors.ENDC}
    Centro de notificaciones
    
  • {Colors.BOLD}SessionManager{Colors.ENDC}
    Gestor de sesiones de trabajo
    
  • {Colors.BOLD}AchievementSystem{Colors.ENDC}
    Sistema de 6 logros desbloqueables
    
  • {Colors.BOLD}BackupManager{Colors.ENDC}
    Gestor de copias de seguridad
    
  • {Colors.BOLD}ReportGenerator{Colors.ENDC}
    Generador de reportes

Presiona ENTER para volver al menú...
""")
    input()

def open_documentation():
    """Abre la documentación."""
    doc_file = "NUEVAS_FUNCIONES.md"
    if os.path.exists(doc_file):
        if os.name == 'nt':
            os.startfile(doc_file)
        else:
            os.system(f"cat {doc_file}")
    else:
        print(f"{Colors.RED}❌ Archivo {doc_file} no encontrado{Colors.ENDC}")

def open_code_viewer():
    """Permite ver los archivos de código."""
    print(f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}💻 EXPLORADOR DE CÓDIGO{Colors.ENDC}
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.ENDC}

{Colors.GREEN}Archivos disponibles:{Colors.ENDC}

1. src/features/enhanced_ui.py (Componentes UI)
2. src/features/advanced_analytics.py (Análisis)
3. src/utils/advanced_utilities.py (Utilidades)
4. ui/modern_ui.py (UI Principal)
5. demo_new_features.py (Demostración)

{Colors.YELLOW}Selecciona un número (1-5) o 0 para volver:{Colors.ENDC} """)
    
    files = [
        "src/features/enhanced_ui.py",
        "src/features/advanced_analytics.py",
        "src/utils/advanced_utilities.py",
        "ui/modern_ui.py",
        "demo_new_features.py"
    ]
    
    try:
        choice = input().strip()
        if choice == '0':
            return
        
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            file_path = files[idx]
            if os.path.exists(file_path):
                if os.name == 'nt':
                    os.system(f"notepad {file_path}")
                else:
                    os.system(f"less {file_path}")
            else:
                print(f"{Colors.RED}❌ Archivo no encontrado{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.RED}❌ Opción inválida{Colors.ENDC}")
    
    input("Presiona ENTER para volver...")

def run_modern_ui():
    """Ejecuta la UI moderna."""
    print(f"{Colors.GREEN}Abriendo UI moderna...{Colors.ENDC}")
    try:
        subprocess.Popen([sys.executable, "ui/modern_ui.py"])
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
    input("Presiona ENTER para volver...")

def run_demo():
    """Ejecuta la demostración."""
    print(f"{Colors.GREEN}Ejecutando demostración...{Colors.ENDC}")
    try:
        subprocess.run([sys.executable, "demo_new_features.py"])
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
    input("Presiona ENTER para volver...")

def main():
    """Bucle principal."""
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == '0':
            print(f"{Colors.GREEN}¡Gracias por usar Guardian!{Colors.ENDC}")
            break
        elif choice == '1':
            run_modern_ui()
        elif choice == '2':
            run_demo()
        elif choice == '3':
            open_documentation()
        elif choice == '4':
            open_code_viewer()
        elif choice == '5':
            print(f"{Colors.YELLOW}Pronto: Configuración avanzada{Colors.ENDC}")
            input("Presiona ENTER...")
        elif choice == '6':
            show_info()
        else:
            print(f"{Colors.RED}❌ Opción inválida{Colors.ENDC}")
            input("Presiona ENTER...")

if __name__ == "__main__":
    main()
