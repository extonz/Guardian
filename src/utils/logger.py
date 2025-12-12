"""
Sistema de logging para Guardian.
Guarda todos los eventos en archivos de log.
"""

import os
from datetime import datetime

LOGS_DIR = "logs"

def ensure_logs_dir():
    """Asegura que la carpeta de logs exista."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

def get_log_file():
    """Retorna el archivo de log del día."""
    ensure_logs_dir()
    date = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOGS_DIR, f"guardian_{date}.log")

def log(message, level="INFO"):
    """Guarda un mensaje de log."""
    ensure_logs_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = get_log_file()
    
    log_message = f"[{timestamp}] [{level}] {message}"
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"Error al escribir log: {e}")

def log_block(app_name):
    """Registra un bloqueo de app."""
    log(f"App bloqueada: {app_name}", "BLOCK")

def log_close(app_name):
    """Registra cierre de app."""
    log(f"App cerrada: {app_name}", "CLOSE")

def log_error(message):
    """Registra un error."""
    log(message, "ERROR")

def log_info(message):
    """Registra información general."""
    log(message, "INFO")

def read_logs(days=1):
    """Lee los logs de los últimos N días."""
    from datetime import timedelta
    
    logs = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = os.path.join(LOGS_DIR, f"guardian_{date}.log")
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs.extend(f.readlines())
            except Exception as e:
                print(f"Error al leer logs: {e}")
    
    return logs

def clear_old_logs(days=7):
    """Borra logs más antiguos de N días."""
    from datetime import timedelta
    import os
    
    ensure_logs_dir()
    cutoff_date = (datetime.now() - timedelta(days=days)).timestamp()
    
    try:
        for filename in os.listdir(LOGS_DIR):
            filepath = os.path.join(LOGS_DIR, filename)
            if os.path.isfile(filepath):
                if os.path.getmtime(filepath) < cutoff_date:
                    os.remove(filepath)
    except Exception as e:
        print(f"Error al limpiar logs: {e}")
