# Script para reorganizar Guardian
# Ejecutar: python organize.py

import os
import shutil

# Mapeo: archivo -> carpeta destino
FILE_MAPPING = {
    # Core
    'monitor.py': 'src/core/',
    'utils.py': 'src/core/',
    'window_detector.py': 'src/core/',
    
    # Features
    'gamification.py': 'src/features/',
    'ml_analyzer.py': 'src/features/',
    'zen_mode.py': 'src/features/',
    'scheduler.py': 'src/features/',
    'reports.py': 'src/features/',
    
    # Security
    'security.py': 'src/security/',
    'blocker.py': 'src/security/',
    'whitelist.py': 'src/security/',
    
    # Notifications
    'alert_system.py': 'src/notifications/',
    
    # Integrations
    'api.py': 'src/integrations/',
    'dashboard.py': 'src/integrations/',
    'import_export.py': 'src/integrations/',
    
    # Utils
    'config.py': 'src/utils/',
    'logger.py': 'src/utils/',
    'settings_manager.py': 'src/utils/',
    
    # UI
    'main.py': 'ui/',
    'dashboard.html': 'ui/',
}

# Crear carpetas si no existen
for folder in set(FILE_MAPPING.values()):
    os.makedirs(folder, exist_ok=True)

# Mover archivos
for file, dest in FILE_MAPPING.items():
    if os.path.exists(file):
        shutil.move(file, os.path.join(dest, file))
        print(f"✓ {file} -> {dest}")

print("\n✓ Archivos reorganizados!")
print("\nNueva estructura:")
print("""
guardian/
├── src/
│   ├── core/
│   │   ├── monitor.py
│   │   ├── utils.py
│   │   ├── window_detector.py
│   ├── features/
│   │   ├── gamification.py
│   │   ├── ml_analyzer.py
│   │   ├── zen_mode.py
│   │   ├── scheduler.py
│   │   ├── reports.py
│   ├── security/
│   │   ├── security.py
│   │   ├── blocker.py
│   │   ├── whitelist.py
│   ├── notifications/
│   │   ├── alert_system.py
│   ├── integrations/
│   │   ├── api.py
│   │   ├── dashboard.py
│   │   ├── import_export.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── settings_manager.py
├── ui/
│   ├── main.py
│   ├── dashboard.html
├── data/
├── logs/
├── requirements.txt
""")
