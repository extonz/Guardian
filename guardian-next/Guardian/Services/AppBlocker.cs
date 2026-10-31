using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.Services
{
    // Reversible, foreground-only soft blocking. Never kills a process.
    public class AppBlocker : IAppBlocker
    {
        private readonly IActiveWindowMonitor _monitor;
        private readonly List<BlockRule> _rules = new();
        private readonly object _gate = new();
        private bool _isRunning;

        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll", SetLastError = true)]
        private static extern uint GetWindowThreadProcessId(IntPtr window, out uint processId);
        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr window, int command);
        private const int SwMinimize = 6;

        private static readonly HashSet<string> Protected = new(StringComparer.OrdinalIgnoreCase)
        {
            "guardian", "explorer", "dwm", "csrss", "winlogon", "services",
            "lsass", "smss", "svchost", "taskmgr", "sihost", "system",
            "applicationframehost", "shellexperiencehost", "startmenuexperiencehost"
        };

        public AppBlocker(IActiveWindowMonitor monitor) => _monitor = monitor;

        public void Start()
        {
            if (_isRunning) return;
            _monitor.WindowChanged += OnWindowChanged;
            _isRunning = true;
        }

        public void Stop()
        {
            _isRunning = false;
            _monitor.WindowChanged -= OnWindowChanged;
        }

        public void AddRule(BlockRule rule)
        {
            var name = Normalize(rule.ProcessName);
            if (string.IsNullOrWhiteSpace(name) || Protected.Contains(name))
                return;
            lock (_gate)
            {
                _rules.RemoveAll(r => Normalize(r.ProcessName).Equals(name, StringComparison.OrdinalIgnoreCase));
                _rules.Add(rule);
            }
        }

        public void RemoveRule(BlockRule rule)
        {
            lock (_gate)
                _rules.RemoveAll(r => Normalize(r.ProcessName).Equals(Normalize(rule.ProcessName), StringComparison.OrdinalIgnoreCase));
        }

        private static string Normalize(string? name)
        {
            var value = (name ?? "").Trim();
            return value.EndsWith(".exe", StringComparison.OrdinalIgnoreCase) ? value[..^4] : value;
        }

        private void OnWindowChanged(object? sender, WindowChangedEventArgs e)
        {
            if (!_isRunning) return;
            var name = Normalize(e.ProcessName);
            lock (_gate)
            {
                if (!_rules.Any(r => r.IsActive && Normalize(r.ProcessName).Equals(name, StringComparison.OrdinalIgnoreCase)))
                    return;
            }

            // Only minimize the currently foreground window, and verify its PID.
            // Never close every window belonging to a process or terminate it.
            try
            {
                var window = GetForegroundWindow();
                if (window == IntPtr.Zero) return;
                GetWindowThreadProcessId(window, out var pid);
                if (pid == 0) return;
                using var process = Process.GetProcessById(checked((int)pid));
                if (Normalize(process.ProcessName).Equals(name, StringComparison.OrdinalIgnoreCase))
                    ShowWindow(window, SwMinimize);
            }
            catch (Exception ex) when (ex is ArgumentException or InvalidOperationException or System.ComponentModel.Win32Exception or OverflowException)
            {
                // The foreground process may have exited between detection and enforcement.
            }
        }
    }
}
