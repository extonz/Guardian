"""
Módulo de UI mejorada con componentes visuales avanzados.
Proporciona widgets personalizados y temas modernos.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from datetime import datetime

# Colores modernos
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'dark': '#2c3e50',
    'light': '#ecf0f1',
    'card_bg': '#34495e',
    'text': '#ffffff',
}

class ModernButton(tk.Canvas):
    """Botón moderno con hover y animación."""
    def __init__(self, parent, text="", command=None, width=200, height=50,
                 bg_color=COLORS['primary'], hover_color=COLORS['secondary'], **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'],
                        highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.text = text
        self.width = width
        self.height = height
        
        self.rect = self.create_rounded_rectangle(2, 2, width-2, height-2,
                                                  radius=20, fill=bg_color, outline="")
        self.text_id = self.create_text(width/2, height/2, text=text, fill=COLORS['text'],
                                       font=("Segoe UI", 11, "bold"))
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
        """Crea un rectángulo con esquinas redondeadas."""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="arrow")

    def _on_click(self, event):
        if self.command:
            self.command()


class StatCard(tk.Frame):
    """Tarjeta de estadísticas moderna."""
    def __init__(self, parent, title="", value="", icon="📊", color=COLORS['primary'], **kwargs):
        super().__init__(parent, bg=COLORS['card_bg'], **kwargs)
        self.pack_propagate(False)
        
        # Borde superior de color
        border = tk.Frame(self, bg=color, height=4)
        border.pack(fill=tk.X)
        
        # Contenido
        content = tk.Frame(self, bg=COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icono y título
        header = tk.Frame(content, bg=COLORS['card_bg'])
        header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header, text=icon, font=("Arial", 24), bg=COLORS['card_bg']).pack(side=tk.LEFT)
        tk.Label(header, text=title, font=("Segoe UI", 11, "bold"), 
                fg=COLORS['text'], bg=COLORS['card_bg']).pack(side=tk.LEFT, padx=10)
        
        # Valor
        tk.Label(content, text=value, font=("Segoe UI", 24, "bold"),
                fg=color, bg=COLORS['card_bg']).pack(fill=tk.X)


class GradientFrame(tk.Canvas):
    """Frame con gradiente de fondo."""
    def __init__(self, parent, color1=COLORS['primary'], color2=COLORS['secondary'], **kwargs):
        super().__init__(parent, **kwargs, highlightthickness=0)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Crear gradiente simple
        r1 = int(self.color1[1:3], 16)
        g1 = int(self.color1[3:5], 16)
        b1 = int(self.color1[5:7], 16)
        
        r2 = int(self.color2[1:3], 16)
        g2 = int(self.color2[3:5], 16)
        b2 = int(self.color2[5:7], 16)
        
        for i in range(height):
            ratio = i / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, fill=color, tags="gradient")


class ModernTabbedUI:
    """Interfaz tabulada moderna."""
    def __init__(self, parent):
        self.parent = parent
        self.tabs = {}
        self.buttons = {}
        
        # Frame para botones de tabs
        self.tab_buttons_frame = tk.Frame(parent, bg=COLORS['dark'])
        self.tab_buttons_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Frame para contenido
        self.content_frame = tk.Frame(parent, bg=COLORS['dark'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    def add_tab(self, name, label):
        """Agrega una nueva pestaña."""
        # Botón
        btn = tk.Button(self.tab_buttons_frame, text=label, font=("Segoe UI", 11, "bold"),
                       bg=COLORS['card_bg'], fg=COLORS['text'], 
                       relief=tk.FLAT, padx=20, pady=10,
                       command=lambda: self.show_tab(name))
        btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.buttons[name] = btn
        
        # Frame de contenido
        frame = tk.Frame(self.content_frame, bg=COLORS['dark'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tabs[name] = frame
        
        # Ocultar por defecto
        frame.pack_forget()
        
        return frame

    def show_tab(self, name):
        """Muestra una pestaña."""
        # Ocultar todas
        for tab_name, tab_frame in self.tabs.items():
            tab_frame.pack_forget()
            self.buttons[tab_name].config(bg=COLORS['card_bg'])
        
        # Mostrar seleccionada
        self.tabs[name].pack(fill=tk.BOTH, expand=True)
        self.buttons[name].config(bg=COLORS['primary'])


class NotificationBadge(tk.Label):
    """Badge de notificación con animación."""
    def __init__(self, parent, count=0, **kwargs):
        super().__init__(parent, **kwargs)
        self.count = count
        self.update_count()

    def update_count(self, count=None):
        if count is not None:
            self.count = count
        
        if self.count > 0:
            self.config(text=str(self.count), bg=COLORS['danger'], 
                       fg=COLORS['text'], font=("Arial", 10, "bold"),
                       padx=8, pady=4, relief=tk.RAISED)
        else:
            self.config(text="")


class ProgressBar(tk.Canvas):
    """Barra de progreso moderna."""
    def __init__(self, parent, width=300, height=20, bg_color=COLORS['primary'], **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'],
                        highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.progress = 0
        
        # Fondo
        self.create_rounded_rectangle(0, 0, width, height, radius=10,
                                     fill=COLORS['card_bg'], outline="")
        # Progreso
        self.progress_rect = self.create_rounded_rectangle(0, 0, 0, height, radius=10,
                                                          fill=bg_color, outline="")

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def set_progress(self, value):
        """Establece el progreso (0-100)."""
        self.progress = max(0, min(100, value))
        new_width = (self.width * self.progress) / 100
        self.coords(self.progress_rect, 0, 0, new_width, self.height)


class TimeTracker:
    """Rastreador de tiempo de enfoque."""
    def __init__(self):
        self.sessions = []
        self.current_session_start = None

    def start_session(self):
        """Inicia una sesión de enfoque."""
        self.current_session_start = datetime.now()

    def end_session(self):
        """Finaliza la sesión actual."""
        if self.current_session_start:
            duration = (datetime.now() - self.current_session_start).total_seconds() / 60
            self.sessions.append({
                'start': self.current_session_start,
                'duration': duration
            })
            self.current_session_start = None
            return duration
        return 0

    def get_total_focus_time(self):
        """Retorna el tiempo total de enfoque en minutos."""
        return sum(s['duration'] for s in self.sessions)

    def get_session_count(self):
        """Retorna la cantidad de sesiones."""
        return len(self.sessions)


class FocusTimer:
    """Timer de Pomodoro mejorado."""
    def __init__(self, work_minutes=25, break_minutes=5):
        self.work_time = work_minutes * 60
        self.break_time = break_minutes * 60
        self.current_time = self.work_time
        self.is_running = False
        self.is_break = False

    def start(self):
        self.is_running = True

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.current_time = self.work_time
        self.is_break = False

    def toggle_session(self):
        """Alterna entre trabajo y descanso."""
        self.is_break = not self.is_break
        self.current_time = self.break_time if self.is_break else self.work_time

    def get_display_time(self):
        """Retorna el tiempo formateado."""
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        return f"{minutes:02d}:{seconds:02d}"

    def tick(self):
        """Decrementa el timer."""
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            return self.current_time
        return self.current_time
