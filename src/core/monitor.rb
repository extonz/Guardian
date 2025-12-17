require 'sys/proctable'
require 'json'

class Monitor
  def initialize
    @blocked_apps = ['TikTok', 'Instagram', 'Facebook', 'YouTube']
    @blocks_today = 0
  end
  
  def check_apps
    current_processes.each do |process|
      if blocked?(process)
        block_app(process)
        @blocks_today += 1
      end
    end
  end
  
  def current_processes
    Sys::ProcTable.ps.map { |p| p.comm.downcase }
  rescue
    []
  end
  
  def blocked?(process)
    @blocked_apps.any? { |app| process.include?(app.downcase) }
  end
  
  def block_app(app)
    # TODO: Implement system-level blocking
    puts "🚫 Bloqueado: #{app}"
  end
  
  def blocks_today
    @blocks_today
  end
end
