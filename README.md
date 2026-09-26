# Guardian

Un asistente de bienestar digital para ayudarte a mantener el enfoque. Guardian permite supervisar el uso de aplicaciones, gestionar distracciones y consultar estadísticas de productividad, con almacenamiento local.

## Características

- Seguimiento de actividad y sesiones de enfoque
- Bloqueo de aplicaciones y lista de permitidas
- Metas diarias, horarios y modo Zen
- Estadísticas, alertas y reportes exportables
- Perfiles y sistema de logros

## Requisitos

- Python 3.8+
- Tkinter

## Instalación

```bash
git clone https://github.com/extonz/Guardian.git
cd Guardian
pip install -r requirements.txt
```

### Releases / Binarios Ejecutables

**Guardian** se distribuye como binario a través de GitHub Releases para mayor comodidad y uso directo, con la facilidad de crear compilados mediante GitHub Actions de manera automática al subir los tags de release.
Simplemente diríjase a la sección "Releases" del repositorio, y descargue el archivo respectivo para su sistema operativo.

### Uso

```bash
# Ejecutar Guardian (RECOMENDADO)
python main.py
```

## Documentación

Consulta la [Wiki](https://github.com/extonz/Guardian/wiki) para la guía en inglés y la [carpeta docs](docs/) para documentación adicional.

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
│   ├── core/
│   │   └── monitor.py             # Monitoreo de apps
│   ├── utils/
│   │   └── settings_manager.py    # Gestión de configuración
│   ├── logger.py              # Sistema de logs
│   ├── daily_goals.py         # Metas diarias
│   ├── smart_alerts.py        # Alertas inteligentes
│   ├── session_tracker.py     # Historial de sesiones
│   ├── alert_system.py        # Alertas del sistema (sonidos)
│   ├── config.py              # Configuración (Apps bloqueadas)
│   ├── window_detector.py     # Gestor de ventanas bloqueadas
│   ├── whitelist.py           # Excepciones
│   └── utils.py               # Herramientas de utilidad
├── config/                     # Configuración (al autogenerarse)
├── .github/workflows/           # Acciones de build automatizadas
├── tests/                      # Tests unitarios
├── requirements.txt            # Dependencias
├── buildozer.spec              # Build spec de Android
├── LICENSE                     # Licencia MIT
└── README.md                   # Este archivo
```
## Contribuir

Las contribuciones son bienvenidas. Abre un [issue](https://github.com/extonz/Guardian/issues) para informar de errores o sugerir mejoras.

## Contacto

[hello@noel.work.gd](mailto:hello@noel.work.gd)

## Licencia

[MIT](LICENSE)

---

Creado por [Noel (@extonz)](https://github.com/extonz).
