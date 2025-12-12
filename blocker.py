import tkinter as tk
import webbrowser
from src.security.whitelist import ALLOWED_DOMAINS
from src.core.utils import kill_process_by_name
from src.utils.config import BLOCKED_APPS, WARNING_TIME
from urllib.parse import urlparse
import os
import platform

# Sistema de bloqueo de sitios web por hosts file
HOSTS_FILE_WINDOWS = r"C:\Windows\System32\drivers\etc\hosts"
HOSTS_FILE_LINUX = "/etc/hosts"
HOSTS_FILE_MAC = "/private/etc/hosts"

def get_hosts_file():
    """Retorna la ruta del archivo hosts según el SO."""
    system = platform.system()
    if system == "Windows":
        return HOSTS_FILE_WINDOWS
    elif system == "Linux":
        return HOSTS_FILE_LINUX
    elif system == "Darwin":
        return HOSTS_FILE_MAC
    return None

def is_url_allowed(url):
    if not url:
        return False
    parsed = urlparse(url)
    netloc = parsed.netloc + parsed.path
    for entry in ALLOWED_DOMAINS:
        if entry['type'] == 'exact' and netloc.startswith(entry['domain']):
            return True
        elif entry['type'] == 'subdomain' and entry['domain'] in netloc:
            return True
    return False

def block_site(domain):
    """Bloquea un dominio redirigiendo a 127.0.0.1."""
    hosts_file = get_hosts_file()
    if not hosts_file:
        return False, "SO no soportado"
    
    try:
        with open(hosts_file, 'a') as f:
            f.write(f"\n127.0.0.1 {domain}")
            f.write(f"\n127.0.0.1 www.{domain}")
        
        return True, f"Dominio {domain} bloqueado"
    except PermissionError:
        return False, "Se requieren permisos de administrador"
    except Exception as e:
        return False, f"Error: {e}"

def unblock_site(domain):
    """Desbloquea un dominio."""
    hosts_file = get_hosts_file()
    if not hosts_file or not os.path.exists(hosts_file):
        return False, "Archivo hosts no encontrado"
    
    try:
        with open(hosts_file, 'r') as f:
            lines = f.readlines()
        
        with open(hosts_file, 'w') as f:
            for line in lines:
                if f"127.0.0.1 {domain}" not in line and f"127.0.0.1 www.{domain}" not in line:
                    f.write(line)
        
        return True, f"Dominio {domain} desbloqueado"
    except PermissionError:
        return False, "Se requieren permisos de administrador"
    except Exception as e:
        return False, f"Error: {e}"

def get_blocked_sites():
    """Retorna lista de sitios bloqueados."""
    hosts_file = get_hosts_file()
    blocked = []
    
    if not hosts_file or not os.path.exists(hosts_file):
        return blocked
    
    try:
        with open(hosts_file, 'r') as f:
            for line in f.readlines():
                if line.startswith("127.0.0.1") and not line.startswith("#"):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        domain = parts[1]
                        if not domain.startswith("www.") and domain not in blocked:
                            blocked.append(domain)
    except Exception as e:
        print(f"Error leyendo sitios bloqueados: {e}")
    
    return blocked

def block_app(app_name):
    root = tk.Tk()
    root.title("Aplicación bloqueada")
    root.geometry("400x120")
    label = tk.Label(root, text=f"La aplicación {app_name} está bloqueada.\nCerrando en {WARNING_TIME} segundos...", font=("Arial", 11))
    label.pack(pady=20)
    root.after(WARNING_TIME * 1000, lambda: (kill_process_by_name(app_name), root.destroy()))
    root.mainloop()

def block_if_not_allowed(url):
    if not is_url_allowed(url):
        webbrowser.open("about:blank")
        return True
    return False
