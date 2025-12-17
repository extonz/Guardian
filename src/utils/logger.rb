require 'logger'
require 'fileutils'

class GuardianLogger
  LOG_DIR = File.join(__dir__, '../../logs')
  
  def initialize
    FileUtils.mkdir_p(LOG_DIR)
    @logger = ::Logger.new(File.join(LOG_DIR, "guardian.log"))
    @logger.level = ::Logger::INFO
    @logger.formatter = proc do |severity, datetime, progname, msg|
      "#{datetime} [#{severity}] #{msg}\n"
    end
  end
  
  def info(message)
    @logger.info(message)
  end
  
  def warn(message)
    @logger.warn(message)
  end
  
  def error(message)
    @logger.error(message)
  end
  
  def debug(message)
    @logger.debug(message)
  end
end
