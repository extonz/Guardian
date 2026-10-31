using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Guardian.Core;

namespace Guardian.Services
{
    public class ActiveWindowMonitor : IActiveWindowMonitor
    {
        public event EventHandler<WindowChangedEventArgs>? WindowChanged;

        private CancellationTokenSource? _cancellationTokenSource;
        private string _lastProcessName = string.Empty;
        private string _lastWindowTitle = string.Empty;

        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll")]
        private static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);

        public void StartMonitoring()
        {
            if (_cancellationTokenSource != null) return;

            _cancellationTokenSource = new CancellationTokenSource();

            // Run loop in background
            Task.Run(async () => await MonitorLoopAsync(_cancellationTokenSource.Token));
        }

        public void StopMonitoring()
        {
            _cancellationTokenSource?.Cancel();
            _cancellationTokenSource?.Dispose();
            _cancellationTokenSource = null;
        }

        private async Task MonitorLoopAsync(CancellationToken token)
        {
            while (!token.IsCancellationRequested)
            {
                try
                {
                    if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                    {
                        var handle = GetForegroundWindow();

                        if (handle != IntPtr.Zero)
                        {
                            GetWindowThreadProcessId(handle, out uint processId);

                            if (processId > 0)
                            {
                                using var process = Process.GetProcessById((int)processId);
                                string processName = process.ProcessName;

                                const int nChars = 256;
                                StringBuilder builder = new StringBuilder(nChars);
                                string windowTitle = "";
                                if (GetWindowText(handle, builder, nChars) > 0)
                                {
                                    windowTitle = builder.ToString();
                                }

                                if (processName != _lastProcessName || windowTitle != _lastWindowTitle)
                                {
                                    _lastProcessName = processName;
                                    _lastWindowTitle = windowTitle;

                                    WindowChanged?.Invoke(this, new WindowChangedEventArgs
                                    {
                                        ProcessName = processName,
                                        WindowTitle = windowTitle
                                    });
                                }
                            }
                        }
                    }
                    else
                    {
                        // On Linux/Mac, emit dummy events if needed for testing, or just do nothing.
                        // Guardian v6 handles cross-platform, but this Next version targets Windows WPF.
                        if (_lastProcessName != "MockProcess")
                        {
                            _lastProcessName = "MockProcess";
                            _lastWindowTitle = "Mock Window";
                            WindowChanged?.Invoke(this, new WindowChangedEventArgs
                            {
                                ProcessName = _lastProcessName,
                                WindowTitle = _lastWindowTitle
                            });
                        }
                    }
                }
                catch (Exception)
                {
                    // Ignore transient exceptions like process exiting during GetProcessById
                }

                await Task.Delay(1000, token); // Check every second
            }
        }
    }
}
