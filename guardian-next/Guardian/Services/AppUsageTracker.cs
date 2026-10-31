using System;
using System.Threading.Tasks;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.Services
{
    public class AppUsageTracker
    {
        private readonly IActiveWindowMonitor _monitor;
        private readonly IRepository _repository;
        private AppUsage? _currentUsage;

        public AppUsageTracker(IActiveWindowMonitor monitor, IRepository repository)
        {
            _monitor = monitor;
            _repository = repository;
        }

        public void Start()
        {
            _monitor.WindowChanged += OnWindowChanged;
        }

        public void Stop()
        {
            _monitor.WindowChanged -= OnWindowChanged;
            EndCurrentUsage();
        }

        private async void OnWindowChanged(object? sender, WindowChangedEventArgs e)
        {
            if (_currentUsage?.ProcessName == e.ProcessName)
            {
                // Title might have changed, but process is the same. We could log this if needed,
                // but for simple duration tracking, we ignore it.
                return;
            }

            await EndCurrentUsageAsync();

            _currentUsage = new AppUsage
            {
                ProcessName = e.ProcessName,
                WindowTitle = e.WindowTitle,
                StartTime = DateTime.Now
            };
        }

        private void EndCurrentUsage()
        {
            EndCurrentUsageAsync().Wait();
        }

        private async Task EndCurrentUsageAsync()
        {
            if (_currentUsage != null)
            {
                _currentUsage.EndTime = DateTime.Now;

                // Only save if duration is meaningful (e.g. > 1 second)
                if (_currentUsage.Duration.TotalSeconds >= 1)
                {
                    await _repository.SaveAppUsageAsync(_currentUsage);
                }

                _currentUsage = null;
            }
        }
    }
}
