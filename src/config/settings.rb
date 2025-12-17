require 'json'
require 'fileutils'

class Settings
  CONFIG_PATH = File.join(__dir__, '../../config/guardian_settings.json')
  
  def self.load
    if File.exist?(CONFIG_PATH)
      JSON.parse(File.read(CONFIG_PATH), symbolize_names: true)
    else
      default_settings
    end
  end
  
  def self.save(settings)
    FileUtils.mkdir_p(File.dirname(CONFIG_PATH))
    File.write(CONFIG_PATH, JSON.pretty_generate(settings))
  end
  
  def self.default_settings
    {
      current_profile: 'default',
      blocked_apps: ['TikTok', 'Instagram', 'Facebook'],
      whitelist_domains: ['github.com', 'stackoverflow.com'],
      pomodoro_minutes: 25,
      break_minutes: 5,
      daily_limit_minutes: 480,
      profiles: {
        'default' => { blocked_apps: [], hours: [] },
        'work' => { blocked_apps: ['TikTok', 'Instagram'], hours: ['09:00-17:00'] },
        'study' => { blocked_apps: ['TikTok', 'Instagram', 'YouTube'], hours: ['14:00-20:00'] }
      }
    }
  end
end
