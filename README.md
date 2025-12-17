<p align="center">
  <img src="https://share.creavite.co/6941b2f007e523c90b19fd8c.gif" width="450">
</p>

# 🛡️ Guardian - Sistema de Bienestar Digital

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)]()
  
> [!IMPORTANT]
> If you are looking for the english README, go to Wiki of Guardian (https://github.com/extonz/Guardian/wiki)

## 📋 Descripción

**Guardian** es un sistema integral de monitoreo y bienestar digital diseñado para mejorar la productividad y la salud digital. Bloquea aplicaciones distractoras, analiza patrones de comportamiento y proporciona insights personalizados para mantener el enfoque.

## ✨ Características Principales

### 🎯 Metas Diarias (v5.1 ✨ NUEVO)
- Establece objetivos de tiempo de enfoque
- Monitorea límites de distracciones
- Progreso en tiempo real
- Alertas cuando alcanzas metas

### 📊 Análisis Avanzado
- Score automático de productividad (0-100)
- Análisis de patrones diarios/semanales
- Identificación de horas pico de distracción
- Insights personalizados automáticos
- Análisis de tendencias de productividad
- Métricas de bienestar digital

### 🚨 Alertas Inteligentes (v5.1 ✨ NUEVO)
- Notificaciones contextuales según tu actividad
- Sugerencias de descansos automáticas
- Alertas sobre muchas distracciones
- Recomendaciones de modo Zen
- Resumen diario de productividad

### 📈 Reportes Exportables (v5.1 ✨ NUEVO)
- Exporta a JSON, CSV, TXT
- Reportes semanales con análisis
- Recomendaciones personalizadas
- Descarga tu historial completo

### 📚 Historial de Sesiones (v5.1 ✨ NUEVO)
- Rastreo automático de sesiones de trabajo
- Estadísticas de sesiones recientes
- Mejores sesiones registradas

### 🎨 UI Profesional (v5.1+ ✨ NUEVO)
- Interfaz oscura moderna (dark theme)
- Diálogos personalizados profesionales
- Sin componentes predeterminados de Windows
- Tema de colores consistente (cyan/verde/naranja)
- Iconografía con emojis mejorada

### 👤 Gestión de Perfiles (v5.1+ ✨ NUEVO)
- Crear múltiples perfiles de usuario
- Configuración independiente por perfil
- Guardar/cargar perfiles persistentes
- Perfil por defecto incluido

### ✅ Whitelist Avanzada (v5.1+ ✨ NUEVO)
- Permitir aplicaciones específicas
- Permitir sitios web específicos
- Gestor dual (Apps + Websites)
- Persistencia en JSON

### ⏰ Gestor de Horarios (v5.1+ ✨ NUEVO)
- Configurar horario de trabajo
- Duración de descansos personalizables
- Sincronización automática
- Activación por hora

### 🧘 Modo Zen (v5.1+ ✨ NUEVO)
- Activación de modo enfoque total
- Duración configurable
- Silencia todas las notificaciones
- Ambiente limpio para concentrarse
- Racha de productividad

### 🏆 Gamificación
- Sistema de 6 logros desbloqueables
- Tracking de racha
- Badges y notificaciones
- Motivación visual

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- tkinter (incluido en Python)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/extonz/Guardian.git
cd Guardian

# Instalar dependencias
pip install -r requirements.txt
```

### Uso

```bash
# Ejecutar Guardian (RECOMENDADO)
python main.py
```

## 🎮 Guía de la Interfaz v5.1+

### Pantalla Principal

**Fila 1 - Controles Principales:**
- **▶ Iniciar** - Inicia el monitoreo de Guardian
- **⏹ Detener** - Detiene el monitoreo
- **📊 Estadísticas** - Ver análisis de productividad
- **🚨 Alertas** - Ver alertas inteligentes
- **🎯 Metas** - Gestionar metas diarias
- **📈 Exportar** - Exportar reportes

**Fila 2 - Funciones Avanzadas:**
- **👤 Perfiles** - Crear y gestionar múltiples perfiles
- **✅ Whitelist** - Permitir apps/sitios específicos
- **⏰ Horario** - Configurar horario de trabajo
- **🧘 Zen Mode** - Activar modo enfoque total
- **📋 Reportes** - Ver análisis detallados

### Uso de Funcionalidades v5.1+

#### 👤 Gestión de Perfiles
1. Haz clic en "👤 Perfiles"
2. Selecciona un perfil o crea uno nuevo
3. Personaliza configuración por perfil
4. Los cambios se guardan automáticamente en `config/profiles.json`

#### ✅ Whitelist Manager
1. Haz clic en "✅ Whitelist"
2. Elige entre "Aplicaciones" o "Sitios Web"
3. Agrega URLs o nombres de aplicaciones
4. Los cambios se guardan en `config/whitelist.json`

#### ⏰ Gestor de Horarios
1. Haz clic en "⏰ Horario"
2. Configura hora de inicio y fin (HH:MM)
3. Establece duración de descansos en minutos
4. Haz clic en "Guardar"

#### 🧘 Modo Zen
1. Haz clic en "🧘 Zen Mode"
2. Ingresa duración en minutos
3. Haz clic en "Activar"
4. Disfruta del enfoque total

#### 📋 Reportes Detallados
1. Haz clic en "📋 Reportes"
2. Visualiza análisis de 7 días
3. Lee recomendaciones personalizadas
4. Exporta si es necesario

## 📁 Estructura del Proyecto

```
Guardian/
├── main.py                      # Punto de entrada principal
├── src/                         # Código fuente
│   ├── monitor.py             # Monitoreo de apps
│   ├── blocker.py             # Sistema de bloqueo
│   ├── settings_manager.py    # Gestión de configuración
│   ├── logger.py              # Sistema de logs
│   ├── reports.py             # Generador de reportes
│   ├── scheduler.py           # Planificador
│   ├── gamification.py        # Sistema de logros
│   ├── zen_mode.py            # Modo zen
│   ├── security.py            # Detección de seguridad
│   ├── ml_analyzer.py         # Análisis ML
│   ├── advanced_stats.py      # Estadísticas avanzadas ✨
│   ├── daily_goals.py         # Metas diarias ✨
│   ├── smart_alerts.py        # Alertas inteligentes ✨
│   ├── session_tracker.py     # Historial de sesiones ✨
│   ├── advanced_exporter.py   # Exportación avanzada ✨
│   ├── ui/
│   │   ├── modern_ui.py
│   │   └── dashboard.html
│   ├── examples/
│   └── tools/
├── config/                     # Configuración
│   ├── guardian_settings.json
│   ├── guardian_stats.json
│   └── daily_goals.json
├── data/                       # Datos
│   └── sessions_history.json
├── docs/                       # Documentación
│   ├── CHANGELOG.md
│   ├── FEATURES.md
│   └── INSTALL.md
├── requirements.txt            # Dependencias
├── LICENSE                     # Licencia MIT
└── README.md                   # Este archivo
```

## 🎯 Nuevas Funcionalidades (v5.1)

### 1️⃣ Metas Diarias
```python
from src.daily_goals import DailyGoalsManager

goals = DailyGoalsManager()

# Establecer metas
goals.set_goal("focus_time", 120)      # 120 minutos de enfoque
goals.set_goal("blocks_limit", 10)     # Máximo 10 bloqueos

# Verificar progreso
progress = goals.check_goal_progress(daily_stats)
print(f"Progreso enfoque: {progress['focus_time']['percentage']}%")
```

### 2️⃣ Estadísticas Avanzadas
```python
from src.advanced_stats import AdvancedStats

stats = AdvancedStats()

# Tendencias de productividad
trend = stats.get_productivity_trend(days=7)
print(f"Tendencia: {trend['trend']}")

# Mejores horas del día
best_hours = stats.get_best_focus_hours()
print(f"Mejor hora: {best_hours[0]}")

# Patrones de distracción
patterns = stats.get_distraction_patterns()
print(f"Apps más distractoras: {patterns['most_distracting_apps']}")

# Métricas de bienestar
health = stats.get_health_metrics()
```

### 3️⃣ Alertas Inteligentes
```python
from src.smart_alerts import SmartAlerts

alerts = SmartAlerts()

# Alertas de productividad
prod_alerts = alerts.check_productivity_alerts(stats)

# Alerta de bienestar
wellness = alerts.get_wellness_alert(stats)

# Resumen diario
summary = alerts.get_daily_summary_alert(stats)

for alert in prod_alerts:
    print(alerts.format_alert_message(alert))
```

### 4️⃣ Historial de Sesiones
```python
from src.session_tracker import SessionTracker

tracker = SessionTracker()

# Iniciar sesión de trabajo
tracker.start_session("work")
# ... trabaja ...
tracker.end_session()

# Obtener estadísticas
session_stats = tracker.get_session_stats(days=7)
print(f"Sesiones esta semana: {session_stats['sessions_count']}")

# Mejores sesiones
best = tracker.get_best_sessions(limit=5)

# Insights
insights = tracker.get_session_insights()
```

### 5️⃣ Exportación Avanzada
```python
from src.advanced_exporter import AdvancedExporter

exporter = AdvancedExporter()

# Exportar en múltiples formatos
json_file = exporter.export_to_json(data, "reporte")
csv_file = exporter.export_to_csv(data_list, "sesiones")
txt_file = exporter.export_to_txt(content, "resumen")

# Generar reporte semanal automático
weekly = exporter.generate_weekly_report(stats_data)
print(f"Reporte guardado: {weekly}")
```

## 📊 Estadísticas del Proyecto

- **Líneas de código**: +2,500
- **Módulos funcionales**: 20+
- **Nuevas funcionalidades v5.1**: 5
- **Logros desbloqueables**: 6
- **Formatos de exportación**: 3 (JSON, CSV, TXT)

## 🔧 Configuración

### Archivo: `config/guardian_settings.json`
```json
{
  "blocked_apps": ["TikTok", "Instagram", "YouTube"],
  "whitelist_domains": ["github.com", "stackoverflow.com"],
  "pomodoro_minutes": 25,
  "break_minutes": 5,
  "daily_limit_minutes": 480,
  "zen_mode_enabled": true
}
```

## 🔐 Seguridad

- Detección de VPN
- Detección de pantalla dual
- Detección de máquina virtual
- Lista blanca de aplicaciones
- Sistema de bloqueo a nivel de hosts
- Criptografía de datos sensibles

## 📚 Ejemplos Adicionales

### Análisis de Productividad
```python
from src.advanced_analytics import ProductivityAnalyzer

analyzer = ProductivityAnalyzer()
analyzer.record_block("YouTube")
analyzer.record_focus_session(25, quality=0.95)

stats = analyzer.get_daily_stats()
score = analyzer.get_productivity_score()

print(f"Score: {score}/100")
print(f"Bloques hoy: {stats['blocks_today']}")
```

### Sistema de Logros
```python
from src.advanced_utilities import AchievementSystem

achievements = AchievementSystem()
achievements.unlock_achievement('first_block')
achievements.unlock_achievement('focus_warrior')

progress = achievements.get_unlock_progress()
print(f"Progreso: {progress['percentage']:.1f}%")
```

## 🐛 Reporte de Problemas

Si encuentras un bug:
1. Ve a [Issues](https://github.com/extonz/guardian/issues)
2. Crea un nuevo issue con detalles
3. Incluye los pasos para reproducir

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NewFeature`)
3. Commit tus cambios (`git commit -m 'Add NewFeature'`)
4. Push a la rama (`git push origin feature/NewFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ve [LICENSE](LICENSE)

## 👨‍💻 Autor

**Noel** *aka: extonz* - [GitHub](https://github.com/extonz)

## 🙏 Agradecimientos

- Comunidad de Python
- Inspirado en herramientas de productividad modernas
- Todos los contribuidores

## 📞 Contacto

- 📧 Email: nastasiagar123+support@gmail.com
- 💬 Discussions: [GitHub Discussions](https://github.com/extonz/guardian/discussions)

---

## 📢 DISCLAIMER

Este proyecto puede contener código generado por IA (ChatGPT, Claude, Grok, etc.). Reconozco este hecho. Si tienes dudas sobre esto, no abras un issue, es completamente normal. 

Tambien use codigo open source de GitHub, si eres dueño de algun codigo y lo reconoces en este proyecto, no dudes en contactarme por redes sociales o E-Mail. Lo solucionaremos :) 

---

**¿Te gusta Guardian? ⭐ ¡Dale una estrella en GitHub!**
