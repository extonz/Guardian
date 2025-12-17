require 'date'

class Analytics
  def initialize
    @daily_blocks = {}
    @focus_sessions = []
  end
  
  def record_block(app, timestamp = Time.now)
    date = timestamp.to_date.to_s
    @daily_blocks[date] ||= 0
    @daily_blocks[date] += 1
  end
  
  def record_focus_session(duration_minutes, quality = 1.0)
    @focus_sessions << {
      date: Date.today.to_s,
      duration: duration_minutes,
      quality: quality,
      timestamp: Time.now
    }
  end
  
  def get_daily_stats
    today = Date.today.to_s
    
    {
      blocks_today: @daily_blocks[today] || 0,
      focus_sessions_today: focus_sessions_today,
      total_focus_time: total_focus_time_today
    }
  end
  
  def get_weekly_stats
    week_start = Date.today - Date.today.wday
    
    {
      total_blocks: @daily_blocks.select { |date, _| Date.parse(date) >= week_start }.values.sum,
      avg_blocks_per_day: (weekly_blocks.sum.to_f / 7).round(2),
      best_day: best_focus_day
    }
  end
  
  def get_productivity_score
    blocks_today = @daily_blocks[Date.today.to_s] || 0
    focus_time = total_focus_time_today
    
    # Score = (focus_time / goal) * 100
    # Max score = 100
    goal_minutes = 480 # 8 hours
    
    score = (focus_time.to_f / goal_minutes * 100).round(0).clamp(0, 100)
    score
  end
  
  private
  
  def focus_sessions_today
    @focus_sessions.select { |s| s[:date] == Date.today.to_s }.length
  end
  
  def total_focus_time_today
    @focus_sessions
      .select { |s| s[:date] == Date.today.to_s }
      .map { |s| s[:duration] }
      .sum
  end
  
  def weekly_blocks
    week_start = Date.today - Date.today.wday
    @daily_blocks.select { |date, _| Date.parse(date) >= week_start }.values
  end
  
  def best_focus_day
    @focus_sessions
      .group_by { |s| s[:date] }
      .max_by { |_, sessions| sessions.map { |s| s[:duration] }.sum }
      .first || 'N/A'
  end
end
