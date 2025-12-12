"""
Sistema de importación/exportación de configuración.
Importar apps desde CSV, exportar backups, etc.
"""

import csv
import json
import os
from datetime import datetime
from src.utils.settings_manager import load_settings, save_settings, get_blocked_apps, add_blocked_app

def export_apps_csv(filename='guardian_apps_export.csv'):
    """Exporta lista de apps bloqueadas a CSV."""
    apps = get_blocked_apps()
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['App Name', 'Exported Date', 'Type'])
            
            for app in apps:
                writer.writerow([app, datetime.now().isoformat(), 'blocked'])
        
        return True, f"Apps exportadas a {filename}"
    except Exception as e:
        return False, f"Error exportando: {e}"

def import_apps_csv(filename='apps.csv'):
    """Importa lista de apps desde CSV."""
    try:
        if not os.path.exists(filename):
            return False, f"Archivo {filename} no encontrado"
        
        imported = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'App Name' in row:
                    add_blocked_app(row['App Name'].strip())
                    imported += 1
        
        return True, f"{imported} apps importadas"
    except Exception as e:
        return False, f"Error importando: {e}"

def export_settings_backup(filename=None):
    """Crea backup de toda la configuración."""
    if filename is None:
        filename = f"guardian_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        settings = load_settings()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True, f"Backup guardado en {filename}"
    except Exception as e:
        return False, f"Error guardando backup: {e}"

def import_settings_backup(filename):
    """Restaura configuración desde backup."""
    try:
        if not os.path.exists(filename):
            return False, f"Archivo {filename} no encontrado"
        
        with open(filename, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        save_settings(settings)
        return True, "Configuración restaurada"
    except Exception as e:
        return False, f"Error restaurando: {e}"

def export_profile_config(profile_name, filename=None):
    """Exporta configuración de un perfil específico."""
    if filename is None:
        filename = f"profile_{profile_name}.json"
    
    try:
        settings = load_settings()
        if profile_name not in settings['profiles']:
            return False, f"Perfil {profile_name} no encontrado"
        
        profile_data = settings['profiles'][profile_name]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=4, ensure_ascii=False)
        
        return True, f"Perfil exportado a {filename}"
    except Exception as e:
        return False, f"Error exportando perfil: {e}"

def import_profile_config(profile_name, filename):
    """Importa configuración para un perfil."""
    try:
        if not os.path.exists(filename):
            return False, f"Archivo {filename} no encontrado"
        
        with open(filename, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        settings = load_settings()
        settings['profiles'][profile_name] = profile_data
        save_settings(settings)
        
        return True, f"Perfil {profile_name} importado"
    except Exception as e:
        return False, f"Error importando perfil: {e}"

def create_share_code(profile_name):
    """Crea un código para compartir configuración (base64 encoded)."""
    try:
        import base64
        settings = load_settings()
        if profile_name not in settings['profiles']:
            return False, "Perfil no encontrado"
        
        profile_data = settings['profiles'][profile_name]
        json_data = json.dumps(profile_data)
        code = base64.b64encode(json_data.encode()).decode()
        
        return True, code
    except Exception as e:
        return False, f"Error creando código: {e}"

def import_share_code(profile_name, code):
    """Importa configuración desde código compartido."""
    try:
        import base64
        json_data = base64.b64decode(code.encode()).decode()
        profile_data = json.loads(json_data)
        
        settings = load_settings()
        settings['profiles'][profile_name] = profile_data
        save_settings(settings)
        
        return True, f"Perfil {profile_name} importado desde código"
    except Exception as e:
        return False, f"Error importando código: {e}"
