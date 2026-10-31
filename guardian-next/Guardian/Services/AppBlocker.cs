using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.Services
{
    public class AppBlocker : IAppBlocker
    {
        private readonly IActiveWindowMonitor _monitor;
        private readonly List<BlockRule> _rules = new();
        private bool _isRunning;

        public AppBlocker(IActiveWindowMonitor monitor)
        {
            _monitor = monitor;
        }

        public void Start()
        {
            if (_isRunning) return;
            _isRunning = true;
            _monitor.WindowChanged += OnWindowChanged;
        }

        public void Stop()
        {
            _isRunning = false;
            _monitor.WindowChanged -= OnWindowChanged;
        }

        public void AddRule(BlockRule rule)
        {
            if (!_rules.Any(r => r.ProcessName.Equals(rule.ProcessName, StringComparison.OrdinalIgnoreCase)))
            {
                _rules.Add(rule);
            }
        }

        public void RemoveRule(BlockRule rule)
        {
            var existing = _rules.FirstOrDefault(r => r.ProcessName.Equals(rule.ProcessName, StringComparison.OrdinalIgnoreCase));
            if (existing != null)
            {
                _rules.Remove(existing);
            }
        }

        private void OnWindowChanged(object? sender, WindowChangedEventArgs e)
        {
            if (!_isRunning) return;

            var matchingRule = _rules.FirstOrDefault(r =>
                r.IsActive &&
                r.ProcessName.Equals(e.ProcessName, StringComparison.OrdinalIgnoreCase));

            if (matchingRule != null)
            {
                // Soft block: show notification or minimize (closing might be too aggressive)
                // For this implementation, we will attempt to close the main window of the process.
                try
                {
                    var processes = Process.GetProcessesByName(e.ProcessName);
                    foreach (var process in processes)
                    {
                        if (process.MainWindowHandle != IntPtr.Zero)
                        {
                            process.CloseMainWindow();
                        }
                    }
                }
                catch
                {
                    // Handle failure gracefully
                }
            }
        }
    }
}
