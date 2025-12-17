"""
Sistema de bloqueo y detección de evasión.
Bloquea Task Manager, CMD, PowerShell, detecta VPN, etc.
"""

import psutil
import subprocess
import os
import ctypes
import threading

BLOCKED_SYSTEM_TOOLS = [
    "taskmgr.exe",      # Task Manager
    "cmd.exe",          # Command Prompt
    "powershell.exe",   # PowerShell
    "pwsh.exe",         # PowerShell Core
    "regedit.exe",      # Registry Editor
    "services.msc",     # Services
    "msconfig.exe",     # System Configuration
    "devmgmt.msc",      # Device Manager
    "compmgmt.msc",     # Computer Management
]

def kill_process(process_name):
    """Cierra un proceso por nombre."""
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                proc.kill()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def block_system_tools():
    """Bloquea herramientas de sistema que podrían desactivar Guardian."""
    for tool in BLOCKED_SYSTEM_TOOLS:
        kill_process(tool)

def is_vpn_active():
    """Detecta si hay una VPN activa."""
    try:
        # Buscar conexiones VPN en el registro
        result = subprocess.run(
            ['powershell', '-Command', 
             'Get-VpnConnection | Select-Object -ExpandProperty Name'],
            capture_output=True, text=True, timeout=5
        )
        return len(result.stdout.strip()) > 0
    except Exception as e:
        print(f"Error detectando VPN: {e}")
        return False

def detect_second_monitor():
    """Detecta si hay un segundo monitor conectado."""
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             'Add-Type -TypeDefinition "using System; using System.Runtime.InteropServices; '
             'public class Display { [DllImport(\\"user32.dll\\")] public static extern int GetSystemMetrics(int nIndex); } '
             'public static void Main() { Console.WriteLine(Display.GetSystemMetrics(80)); }"'],
            capture_output=True, text=True, timeout=5
        )
        # Si retorna >1, hay múltiples monitores
        return int(result.stdout.strip()) > 1
    except:
        return False

def is_virtual_machine():
    """Detecta si se ejecuta en una máquina virtual."""
    try:
        # Comprobar si está en Hyper-V
        result = subprocess.run(
            ['powershell', '-Command', 'Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty Model'],
            capture_output=True, text=True, timeout=5
        )
        vm_indicators = ['virtual', 'vmware', 'hyper-v', 'parallels', 'virtualbox', 'qemu']
        return any(indicator in result.stdout.lower() for indicator in vm_indicators)
    except:
        return False

def block_internet_access(block=True):
    """Bloquea acceso a internet (requiere privilegios admin)."""
    try:
        if block:
            # Bloqueando solo apps específicas sería lo ideal
            # Por ahora solo notificamos
            print("⚠️ Bloqueo de internet requiere privilegios elevados")
        return False
    except Exception as e:
        print(f"Error bloqueando internet: {e}")
        return False

def change_wallpaper(image_path):
    """Cambia el wallpaper del escritorio."""
    try:
        if os.path.exists(image_path):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            return True
    except Exception as e:
        print(f"Error cambiando wallpaper: {e}")
    return False

def disable_task_manager(disable=True):
    """Desactiva Task Manager (requiere acceso al registro)."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Policies\System',
                             0, winreg.KEY_WRITE)
        value = 1 if disable else 0
        winreg.SetValueEx(key, 'DisableTaskMgr', 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error desactivando Task Manager: {e}")
    return False

def monitor_system_tools(on_detected=None):
    """Monitorea constantemente herramientas de sistema bloqueadas."""
    def check():
        while True:
            for tool in BLOCKED_SYSTEM_TOOLS:
                if psutil.pid_exists(psutil.pids()):
                    for proc in psutil.process_iter(['name']):
                        if proc.info['name'].lower() == tool.lower():
                            if on_detected:
                                on_detected(tool)
                            kill_process(tool)
            threading.Event().wait(1)
    
    thread = threading.Thread(target=check, daemon=True)
    thread.start()
