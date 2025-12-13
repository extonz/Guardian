# 🚀 Guía de Instalación

## Requisitos del Sistema

- **Python**: 3.8 o superior
- **RAM**: Mínimo 512 MB
- **Disco**: 100 MB disponibles
- **SO**: Windows, macOS, Linux

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/guardian.git
cd guardian
```

### 2. Crear Entorno Virtual (Recomendado)

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar Instalación

```bash
python -c "import tkinter; print('✓ Instalación correcta')"
```

## Configuración Inicial

### Primera Ejecución

```bash
python main.py
```

Esto creará los archivos de configuración necesarios:
- `guardian_settings.json`
- `guardian_stats.json`

### Configurar Apps a Bloquear

Editar `guardian_settings.json`:

```json
{
  "blocked_apps": [
    "TikTok",
    "Instagram",
    "YouTube",
    "Twitch",
    "Discord"
  ]
}
```

### Configurar Whitelist de Dominios

```json
{
  "whitelist_domains": [
    {"domain": "github.com", "type": "exact"},
    {"domain": "stackoverflow.com", "type": "subdomain"},
    {"domain": "python.org", "type": "exact"}
  ]
}
```

## Métodos de Ejecución

### Opción 1: Interfaz Gráfica Moderna (Recomendado)

```bash
python ui/modern_ui.py
```

**Características:**
- Dashboard con 5 pestañas
- Timer Pomodoro integrado
- Monitor de salud visual
- Insights personalizados

### Opción 2: Interfaz Original

```bash
python main.py
```

### Opción 3: Demostración Interactiva

```bash
python demo_new_features.py
```

### Opción 4: Menú Interactivo

```bash
python quick_start.py
```

## Instalación en Diferentes SO

### Windows

```bash
# Descargar Python desde python.org si no lo tienes
# Clonar repositorio
git clone https://github.com/tu-usuario/guardian.git

# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python ui/modern_ui.py
```

**Nota**: Es posible que necesites ejecutar como administrador para el bloqueo de apps.

### macOS

```bash
# Instalar Python 3.8+ si es necesario
brew install python@3.9

# Clonar repositorio
git clone https://github.com/tu-usuario/guardian.git

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python ui/modern_ui.py
```

### Linux

```bash
# Instalar Python y dependencias
sudo apt update
sudo apt install python3-dev python3-pip python3-tk

# Clonar repositorio
git clone https://github.com/tu-usuario/guardian.git

# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python ui/modern_ui.py
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'tkinter'"

**Solución:**
```bash
# Windows
python -m pip install tk

# macOS
brew install python-tk@3.9

# Linux
sudo apt install python3-tk
```

### Error: "Permission denied" al ejecutar en Linux

```bash
chmod +x main.py
./main.py
```

### Guardian no abre interfaz gráfica

**Verificar:**
1. ¿Está activado el entorno virtual?
2. ¿Está instalado tkinter? → `python -m tkinter`
3. ¿Tienes permisos de administrador?

### Las apps no se bloquean

**Verificar:**
1. ¿Está ejecutándose Guardian?
2. ¿Está la app en la lista de bloqueo?
3. ¿Tienes permisos de administrador?
4. ¿El antivirus bloquea los permisos?

## Actualización

Para actualizar a la última versión:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Desinstalación

```bash
# Desactivar entorno virtual
deactivate

# Eliminar carpeta del proyecto
rm -rf guardian

# O simplemente eliminar la carpeta manualmente
```

## Próximos Pasos

1. ✅ Lee la [Documentación de Características](FEATURES.md)
2. ✅ Explora el [Código API](API.md)
3. ✅ Participa en [Discussions](https://github.com/tu-usuario/guardian/discussions)
4. ✅ Reporta [Issues](https://github.com/tu-usuario/guardian/issues)
