require 'json'
require 'date'

class Gamification
  STATS_FILE = File.join(__dir__, '../../config/guardian_stats.json')
  
  def initialize
    @stats = load_stats
  end
  
  def get_status
    {
      points: @stats['points'] || 0,
      level: (@stats['points'] || 0) / 100 + 1,
      streak: @stats['streak'] || 0,
      blocks: @stats['blocks_today'] || 0,
      badges: @stats['badges'] || []
    }
  end
  
  def add_points(amount)
    @stats['points'] = (@stats['points'] || 0) + amount
    check_achievements
    save_stats
  end
  
  def record_block
    @stats['blocks_today'] = (@stats['blocks_today'] || 0) + 1
    add_points(10)
  end
  
  def update_streak
    today = Date.today.to_s
    
    if @stats['last_active'] == today
      return # Already counted today
    elsif @stats['last_active'] == (Date.today - 1).to_s
      @stats['streak'] = (@stats['streak'] || 0) + 1
    else
      @stats['streak'] = 1
    end
    
    @stats['last_active'] = today
    save_stats
  end
  
  def check_achievements
    points = @stats['points'] || 0
    
    achievements = {
      'first_block' => { condition: @stats['blocks_today'] >= 1, reward: 25 },
      'focus_warrior' => { condition: points >= 500, reward: 100 },
      'level_5' => { condition: points >= 500, reward: 50 },
      'daily_champion' => { condition: (@stats['streak'] || 0) >= 7, reward: 200 }
    }
    
    achievements.each do |name, data|
      if data[:condition] && !(@stats['badges'] || []).include?(name)
        (@stats['badges'] ||= []) << name
        add_points(data[:reward])
      end
    end
  end
  
  private
  
  def load_stats
    return JSON.parse(File.read(STATS_FILE), symbolize_names: true) if File.exist?(STATS_FILE)
    
    default_stats
  end
  
  def default_stats
    {
      'points' => 0,
      'level' => 1,
      'streak' => 0,
      'blocks_today' => 0,
      'badges' => [],
      'last_active' => Date.today.to_s
    }
  end
  
  def save_stats
    FileUtils.mkdir_p(File.dirname(STATS_FILE))
    File.write(STATS_FILE, JSON.pretty_generate(@stats))
  end
end
