class Blocker
  HOSTS_FILE_WINDOWS = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
  HOSTS_FILE_UNIX = '/etc/hosts'
  
  def initialize
    @blocked_sites = {}
    @enabled = true
  end
  
  def block_site(domain)
    entry = "127.0.0.1 #{domain}\n"
    
    if windows?
      add_to_hosts(HOSTS_FILE_WINDOWS, entry)
    else
      add_to_hosts(HOSTS_FILE_UNIX, entry)
    end
    
    @blocked_sites[domain] = true
  end
  
  def unblock_site(domain)
    if windows?
      remove_from_hosts(HOSTS_FILE_WINDOWS, domain)
    else
      remove_from_hosts(HOSTS_FILE_UNIX, domain)
    end
    
    @blocked_sites.delete(domain)
  end
  
  def blocked_sites
    @blocked_sites.keys
  end
  
  private
  
  def windows?
    RUBY_PLATFORM.include?('win')
  end
  
  def add_to_hosts(path, entry)
    # Requires admin privileges
    content = File.exist?(path) ? File.read(path) : ''
    File.write(path, content + entry) unless content.include?(entry)
  end
  
  def remove_from_hosts(path, domain)
    return unless File.exist?(path)
    
    content = File.read(path)
    new_content = content.lines.reject { |line| line.include?(domain) }.join
    File.write(path, new_content)
  end
end
