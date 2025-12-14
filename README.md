# 🛡️ Guardian - Sistema de Bienestar Digital

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)]()

If you want to read the English Wiki, go to https://github.com/extonz/Guardian/wiki
## 📋 Descripción

**Guardian** es un sistema integral de monitoreo y bienestar digital diseñado para mejorar la productividad y la salud digital. Bloquea aplicaciones distractoras, analiza patrones de comportamiento y proporciona insights personalizados para mantener el enfoque.

## ✨ Características Principales


### 📊 Análisis Avanzado
- Score automático de productividad (0-100)
- Análisis de patrones diarios/semanales
- Identificación de horas pico de distracción
- Insights personalizados automáticos


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
git clone https://github.com/tu-usuario/guardian.git
cd guardian

# Instalar dependencias
pip install -r requirements.txt
```

### Uso

**Opción 1: Demostración Interactiva**
```bash
python demo_new_features.py
```

**Opción 2: Menú Interactivo**
```bash
python quick_start.py
```

**Opción 3: Interfaz Original** ** RECOMENDADA**
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
guardian/
├── src/                          # Código fuente principal
│   ├── core/                    # Motor central
│   │   ├── monitor.py          # Monitoreo de apps
│   │   ├── utils.py            # Utilidades base
│   │   └── window_detector.py  # Detector de ventanas
│   ├── features/               # Funcionalidades
│   │   ├── gamification.py     # Sistema de logros
│   │   ├── ml_analyzer.py      # Análisis ML
│   │   ├── reports.py          # Generador de reportes
│   │   ├── scheduler.py        # Planificador
│   │   ├── zen_mode.py         # Modo zen
│   │   ├── enhanced_ui.py      # UI avanzada (NUEVO)
│   │   └── advanced_analytics.py # Análisis avanzado (NUEVO)
│   ├── integrations/           # Integraciones
│   │   ├── api.py             # API REST
│   │   ├── dashboard.py       # Dashboard
│   │   ├── import_export.py   # Import/Export
│   │   └── notifications.py   # Notificaciones
│   ├── security/              # Seguridad
│   │   ├── blocker.py        # Sistema de bloqueo
│   │   ├── security.py       # Detección de seguridad
│   │   └── whitelist.py      # Lista blanca
│   ├── notifications/         # Sistema de alertas
│   │   └── alert_system.py   # Sistema de alertas
│   └── utils/                # Utilidades
│       ├── config.py         # Configuración
│       ├── logger.py         # Logger
│       ├── settings_manager.py # Gestor de configuración
│       └── advanced_utilities.py # Utilidades avanzadas (NUEVO)
├── ui/                        # Interfaz de usuario
│   ├── modern_ui.py          # UI moderna (NUEVO)
│   └── dashboard.html        # Dashboard web
├── docs/                      # Documentación
│   ├── README.md             # Este archivo
│   ├── INSTALL.md            # Guía de instalación
│   ├── FEATURES.md           # Lista de características
│   ├── API.md                # Documentación de API
│   └── CONTRIBUTING.md       # Guía de contribución
├── tests/                     # Pruebas
│   └── test_*.py            # Archivos de test
├── data/                      # Datos de la aplicación
│   └── .gitkeep             # Placeholder
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias Python
├── .gitignore                # Archivos ignorados por git
├── LICENSE                    # Licencia del proyecto
└── CHANGELOG.md              # Historial de cambios
```

## 📖 Documentación

- [📘 Guía de Instalación](docs/INSTALL.md)
- [✨ Lista de Características](docs/FEATURES.md)
- [📝 Changelog](CHANGELOG.md)


## 📊 Estadísticas del Proyecto

- **Líneas de código**: +2,000 
- **Componentes UI**: 7
- **Análisis automáticos**: 4
- **Utilidades avanzadas**: 6
- **Logros desbloqueables**: 6

## 🔧 Configuración

### Archivo: `guardian_settings.json`
```json
{
  "blocked_apps": ["TikTok", "Instagram"],
  "whitelist_domains": ["github.com", "stackoverflow.com"],
  "pomodoro_minutes": 25,
  "break_minutes": 5,
  "daily_limit_minutes": 480
}
```

## 🔐 Seguridad

- Detección de VPN
- Detección de pantalla dual
- Detección de máquina virtual
- Lista blanca de aplicaciones
- Sistema de bloqueo a nivel de hosts

## 📚 Ejemplos de Uso

### Análisis de Productividad
```python
from src.features.advanced_analytics import ProductivityAnalyzer

analyzer = ProductivityAnalyzer()

# Registrar eventos
analyzer.record_block("YouTube")
analyzer.record_focus_session(25, quality=0.95)

# Obtener análisis
stats = analyzer.get_daily_stats()
score = analyzer.get_productivity_score()
trends = analyzer.get_weekly_trends()

print(f"Bloques hoy: {stats['blocks_today']}")
print(f"Score de productividad: {score}/100")
```

### Sistema de Logros
```python
from src.utils.advanced_utilities import AchievementSystem

achievements = AchievementSystem()

# Desbloquear logros
achievements.unlock_achievement('first_block')
achievements.unlock_achievement('focus_warrior')

# Ver progreso
progress = achievements.get_unlock_progress()
print(f"Progreso: {progress['percentage']:.1f}%")
```

## 🐛 Reporte de Problemas

Si encuentras un bug:
1. Ve a [Issues](https://github.com/extonz/guardian/issues)
2. Crea un nuevo issue con detalles
3. Incluye los pasos para reproducir

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request


## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ve [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Noel** *aka: extonz*- [GitHub](https://github.com/extonz)

## 🙏 Agradecimientos

- Comunidad de Python
- Inspirado en herramientas de productividad modernas
- Diseño inspirado en aplicaciones profesionales

## 📞 Contacto

- 📧 Email: nastasiagar123+support@gmail.com
- 🐦 Twitter: [@extonz_](https://twitter.com/extonz_)
- 💬 Discussions: [GitHub Discussions](https://github.com/extonz/guardian/discussions)

---

## DISCLAIMER:

Este proyecto puede contener archivos de codigo hechos por una IA. (ChatGPT, Claude, Grok...) 
Reconozco este hecho, asi que porfavor, NO me hagais un Issue o una Discussion por este tema. 
Si es el caso, la borrare. 
Muchas gracias por la compresion! ❤
---

**¿Te gusta Guardian? ⭐ Dale una estrella en GitHub!**
