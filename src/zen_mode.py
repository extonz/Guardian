"""
Modo Zen: Pantalla negra con timer solamente.
Modo enfoque ultra-minimalista.
"""

import tkinter as tk
import threading
from datetime import datetime, timedelta

class ZenMode:
    def __init__(self, minutes=60):
        self.minutes = minutes
        self.seconds_remaining = minutes * 60
        self.paused = False
        self.window = None
    
    def start(self):
        """Inicia modo Zen."""
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.config(bg='#000000')
        self.window.bind('<Escape>', lambda e: self.stop())
        
        # Timer display
        self.timer_label = tk.Label(
            self.window,
            text=self.format_time(self.seconds_remaining),
            font=('Arial', 120, 'bold'),
            fg='#ffffff',
            bg='#000000'
        )
        self.timer_label.pack(expand=True)
        
        # Info
        info_label = tk.Label(
            self.window,
            text="🧘 MODO ZEN - Presiona ESC para salir",
            font=('Arial', 20),
            fg='#666666',
            bg='#000000'
        )
        info_label.pack(pady=20)
        
        # Iniciar countdown
        self.countdown_thread = threading.Thread(target=self.countdown, daemon=True)
        self.countdown_thread.start()
        
        self.window.mainloop()
    
    def countdown(self):
        """Cuenta hacia atrás."""
        while self.seconds_remaining > 0 and self.window:
            if not self.paused:
                self.seconds_remaining -= 1
                try:
                    self.timer_label.config(text=self.format_time(self.seconds_remaining))
                except:
                    break
            threading.Event().wait(1)
        
        if self.window and self.seconds_remaining <= 0:
            try:
                self.window.destroy()
            except:
                pass
    
    def format_time(self, seconds):
        """Formatea tiempo en HH:MM:SS."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def stop(self):
        """Detiene modo Zen."""
        try:
            self.window.destroy()
        except:
            pass

def start_zen_mode(minutes=60):
    """Inicia modo Zen en thread separado."""
    zen = ZenMode(minutes)
    thread = threading.Thread(target=zen.start, daemon=False)
    thread.start()
    return zen
