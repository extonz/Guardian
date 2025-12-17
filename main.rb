#!/usr/bin/env ruby

# Guardian - Sistema de Bienestar Digital (Ruby Edition)
# Main entry point

require 'json'
require 'yaml'
require 'logger'
require 'date'
require 'thread'
require 'tk'
require 'tkinter'

# Load project modules
$LOAD_PATH.unshift(File.expand_path('../src', __FILE__))

require 'config/settings'
require 'core/monitor'
require 'core/blocker'
require 'core/gamification'
require 'utils/logger'
require 'utils/analytics'

class GuardianUI
  attr_accessor :root, :status_label, :log_text, :monitor_running
  
  def initialize
    @root = TkRoot.new { title "🛡️ Guardian - Digital Wellness"; geometry '900x700' }
    @monitor_running = false
    @settings = Settings.load
    @logger = GuardianLogger.new
    @monitor = Monitor.new
    @blocker = Blocker.new
    @gamification = Gamification.new
    @analytics = Analytics.new
    
    setup_ui
  end
  
  def setup_ui
    # Color scheme
    bg_dark = '#1e1e1e'
    bg_light = '#2d2d2d'
    accent = '#3498db'
    text_color = '#ecf0f1'
    
    @root.configure(bg: bg_dark)
    
    # Header
    header = TkFrame.new(@root, bg: accent, height: 80)
    header.pack(fill: :x, padx: 0, pady: 0)
    header.pack_propagate(false)
    
    TkLabel.new(header, text: '🛡️ GUARDIAN', 
                font: 'Segoe UI 24 bold', 
                fg: text_color, 
                bg: accent).pack(side: :left, padx: 20, pady: 15)
    
    TkLabel.new(header, text: 'Digital Wellness System',
                font: 'Segoe UI 10',
                fg: '#bdc3c7',
                bg: accent).pack(side: :left, padx: 20)
    
    # Main frame
    main_frame = TkFrame.new(@root, bg: bg_dark)
    main_frame.pack(fill: :both, expand: true, padx: 15, pady: 15)
    
    # Status label
    @status_label = TkLabel.new(main_frame, 
                                 text: '✓ Guardian listo',
                                 font: 'Segoe UI 11 bold',
                                 fg: '#2ecc71',
                                 bg: bg_dark)
    @status_label.pack(anchor: :w, pady: (0, 10))
    
    # Stats frame
    stats_frame = TkFrame.new(main_frame, bg: bg_light, relief: :raised, borderwidth: 2)
    stats_frame.pack(fill: :x, pady: 10)
    
    @stats_label = TkLabel.new(stats_frame,
                                text: 'Bloques: 0 | Puntos: 0 | Nivel: 1 | Streak: 0 días',
                                font: 'Segoe UI 10',
                                fg: text_color,
                                bg: bg_light)
    @stats_label.pack(padx: 15, pady: 10, anchor: :w)
    
    # Log area
    TkLabel.new(main_frame, text: 'Actividad',
                font: 'Segoe UI 11 bold',
                fg: text_color,
                bg: bg_dark).pack(anchor: :w, pady: (10, 5))
    
    log_frame = TkFrame.new(main_frame, bg: bg_light)
    log_frame.pack(fill: :both, expand: true, pady: 10)
    
    scrollbar = TkScrollbar.new(log_frame, orient: :vertical)
    scrollbar.pack(side: :right, fill: :y)
    
    @log_text = TkText.new(log_frame, 
                            width: 100, 
                            height: 15,
                            bg: bg_light,
                            fg: text_color,
                            font: 'Courier 9',
                            yscrollcommand: scrollbar.command('set'))
    @log_text.pack(side: :left, fill: :both, expand: true)
    scrollbar.command(:set, @log_text.yscrollcommand)
    
    # Control buttons
    button_frame = TkFrame.new(main_frame, bg: bg_dark)
    button_frame.pack(fill: :x, pady: 15)
    
    @btn_start = TkButton.new(button_frame, text: '▶ Iniciar',
                               bg: '#27ae60', fg: text_color,
                               font: 'Segoe UI 11 bold',
                               command: method(:start_monitor),
                               relief: :flat, padx: 20, pady: 10)
    @btn_start.pack(side: :left, padx: 5)
    
    @btn_stop = TkButton.new(button_frame, text: '⏹ Detener',
                              bg: '#e74c3c', fg: text_color,
                              font: 'Segoe UI 11 bold',
                              command: method(:stop_monitor),
                              relief: :flat, padx: 20, pady: 10,
                              state: :disabled)
    @btn_stop.pack(side: :left, padx: 5)
    
    TkButton.new(button_frame, text: '⚙️ Configurar',
                 bg: '#3498db', fg: text_color,
                 font: 'Segoe UI 11 bold',
                 command: method(:open_config),
                 relief: :flat, padx: 20, pady: 10).pack(side: :left, padx: 5)
    
    # Status bar
    status_bar = TkFrame.new(@root, bg: '#2d2d2d', height: 30)
    status_bar.pack(fill: :x, side: :bottom)
    status_bar.pack_propagate(false)
    
    TkLabel.new(status_bar, text: '© 2025 Guardian - Bienestar Digital',
                font: 'Segoe UI 9',
                fg: '#95a5a6',
                bg: '#2d2d2d').pack(anchor: :w, padx: 10, pady: 5)
  end
  
  def update_status(message)
    @status_label.text = message
    @root.update_idletasks
    
    @log_text.insert('end', "#{message}\n")
    @log_text.see('end')
    @log_text.update_idletasks
  end
  
  def update_stats
    stats = @gamification.get_status
    @stats_label.text = "Bloques: #{stats[:blocks]} | Puntos: #{stats[:points]} | Nivel: #{stats[:level]} | Streak: #{stats[:streak]} días"
  end
  
  def start_monitor
    return if @monitor_running
    
    @monitor_running = true
    @btn_start.state = :disabled
    @btn_start.configure(bg: '#95a5a6')
    @btn_stop.state = :normal
    @btn_stop.configure(bg: '#e74c3c')
    
    @logger.info("Guardian iniciado")
    update_status("✓ Guardian iniciado - Monitoreando apps...")
    
    Thread.new { monitor_loop }
  end
  
  def monitor_loop
    while @monitor_running
      @monitor.check_apps
      update_stats
      sleep 1
    end
  end
  
  def stop_monitor
    @monitor_running = false
    @btn_start.state = :normal
    @btn_start.configure(bg: '#27ae60')
    @btn_stop.state = :disabled
    @btn_stop.configure(bg: '#95a5a6')
    
    @logger.info("Guardian detenido")
    update_status("✗ Guardian detenido")
  end
  
  def open_config
    update_status("⚙️ Panel de configuración abierto")
  end
  
  def run
    Tk.mainloop
  end
end

# Start app
if __FILE__ == $0
  app = GuardianUI.new
  app.run
end
