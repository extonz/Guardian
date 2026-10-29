#!/usr/bin/env python3
"""Guardian v6 desktop application."""
from __future__ import annotations
import queue, threading, tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from src.analytics import summary
from src.engine import Monitor
from src.storage import load, save

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GuardianApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Guardian 6")
        self.geometry("1020x700")
        self.minsize(800, 560)
        self.configure(fg_color="#0b0b0d")
        self.events = queue.Queue()
        self.monitor = Monitor(on_event=lambda title: self.events.put(("blocked", title)))
        self.settings = load("settings")
        self._build()
        self.after(200, self._poll)
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _build(self):
        shell = ctk.CTkFrame(self, fg_color="transparent")
        shell.pack(fill="both", expand=True, padx=24, pady=24)
        sidebar = ctk.CTkFrame(shell, width=190, corner_radius=18, fg_color="#141417")
        sidebar.pack(side="left", fill="y", padx=(0, 18)); sidebar.pack_propagate(False)
        ctk.CTkLabel(sidebar, text="◉  GUARDIAN", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=(24, 30))
        for label, callback in [("Dashboard", self._dashboard), ("Zen mode", self._zen), ("Analíticas", self._analytics), ("Ajustes", self._settings)]:
            ctk.CTkButton(sidebar, text=label, anchor="w", fg_color="transparent", hover_color="#26262b", command=callback).pack(fill="x", padx=12, pady=4)
        self.content = ctk.CTkFrame(shell, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)
        self._dashboard()

    def _clear(self):
        for widget in self.content.winfo_children(): widget.destroy()

    def _heading(self, title, subtitle):
        ctk.CTkLabel(self.content, text=title, font=ctk.CTkFont(size=30, weight="bold")).pack(anchor="w", pady=(10, 2))
        ctk.CTkLabel(self.content, text=subtitle, text_color="#a1a1aa").pack(anchor="w", pady=(0, 22))

    def _dashboard(self):
        self._clear(); self._heading("Tu espacio de concentración", "Menos distracciones. Más intención.")
        data = summary()
        grid = ctk.CTkFrame(self.content, fg_color="transparent"); grid.pack(fill="x")
        for label, value in [("Bloqueos detectados", data["blocks"]), ("Minutos de foco", data["focus_minutes"]), ("Sesiones", data["sessions"])]:
            card = ctk.CTkFrame(grid, corner_radius=16, fg_color="#17171b"); card.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=4)
            ctk.CTkLabel(card, text=label, text_color="#a1a1aa").pack(anchor="w", padx=16, pady=(18, 4))
            ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=30, weight="bold")).pack(anchor="w", padx=16, pady=(0, 18))
        ctk.CTkLabel(self.content, text="Monitor", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(28, 10))
        row = ctk.CTkFrame(self.content, fg_color="#17171b", corner_radius=16); row.pack(fill="x")
        ctk.CTkLabel(row, text="Detecta las ventanas configuradas sin cerrar aplicaciones.").pack(side="left", padx=16, pady=18)
        self.monitor_button = ctk.CTkButton(row, text="Detener monitor" if self.monitor.running else "Iniciar monitor", command=self._toggle_monitor); self.monitor_button.pack(side="right", padx=14, pady=12)
        ctk.CTkLabel(self.content, text="Actividad reciente", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", pady=(28, 8))
        for event in load("stats").get("events", [])[-5:][::-1]:
            if isinstance(event, dict): ctk.CTkLabel(self.content, text=f"{event.get('at','')}   ·   {event.get('app','Aplicación')}", text_color="#b4b4bc").pack(anchor="w", pady=3)

    def _toggle_monitor(self):
        if self.monitor.running: self.monitor.stop()
        else: self.monitor.start()
        self._dashboard()

    def _zen(self):
        self.settings = load("settings"); self.settings["zen_mode"] = not self.settings.get("zen_mode", False); save("settings", self.settings)
        messagebox.showinfo("Zen mode", "Modo Zen activado" if self.settings["zen_mode"] else "Modo Zen desactivado")

    def _analytics(self):
        self._clear(); self._heading("Analíticas", "Resumen guardado localmente")
        for key, value in summary().items(): ctk.CTkLabel(self.content, text=f"{key.replace('_',' ').capitalize()}:  {value}", font=ctk.CTkFont(size=18)).pack(anchor="w", pady=8)

    def _settings(self):
        self._clear(); self._heading("Ajustes", "Personaliza qué aplicaciones quieres vigilar")
        apps = ctk.CTkTextbox(self.content, height=190); apps.pack(fill="x", pady=6); apps.insert("1.0", "\n".join(self.settings.get("blocked_apps", [])))
        whitelist = ctk.CTkTextbox(self.content, height=130); whitelist.pack(fill="x", pady=6); whitelist.insert("1.0", "\n".join(self.settings.get("whitelist", [])))
        ctk.CTkLabel(self.content, text="Aplicaciones restringidas (una por línea)").pack(anchor="w")
        ctk.CTkLabel(self.content, text="Whitelist: nunca mostrar avisos para estos títulos").pack(anchor="w")
        def store():
            self.settings["blocked_apps"] = [x.strip() for x in apps.get("1.0", "end").splitlines() if x.strip()]
            self.settings["whitelist"] = [x.strip() for x in whitelist.get("1.0", "end").splitlines() if x.strip()]
            save("settings", self.settings); messagebox.showinfo("Guardian", "Ajustes guardados")
        ctk.CTkButton(self.content, text="Guardar ajustes", command=store).pack(anchor="e", pady=12)

    def _poll(self):
        while True:
            try: kind, title = self.events.get_nowait()
            except queue.Empty: break
            if kind == "blocked": self.title(f"Guardian 6 · Distracción detectada: {title}")
        if self.winfo_exists(): self.after(200, self._poll)

    def _close(self):
        self.monitor.stop()
        self.destroy()

if __name__ == "__main__":
    GuardianApp().mainloop()
