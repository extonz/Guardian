using System;
using Guardian.Models;

namespace Guardian.Core
{
    public class WindowChangedEventArgs : EventArgs
    {
        public string ProcessName { get; set; } = string.Empty;
        public string WindowTitle { get; set; } = string.Empty;
    }

    public interface IActiveWindowMonitor
    {
        event EventHandler<WindowChangedEventArgs> WindowChanged;
        void StartMonitoring();
        void StopMonitoring();
    }
}
