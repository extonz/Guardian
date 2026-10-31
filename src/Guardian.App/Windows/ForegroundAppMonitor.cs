using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security;
using System.ComponentModel;

namespace Guardian.App.Windows;

internal static class ForegroundAppMonitor
{
    [DllImport("user32.dll")]
    private static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", SetLastError = true)]
    private static extern uint GetWindowThreadProcessId(IntPtr windowHandle, out uint processId);

    public static (IntPtr WindowHandle, string? ProcessName) Read()
    {
        var windowHandle = GetForegroundWindow();
        if (windowHandle == IntPtr.Zero)
            return (IntPtr.Zero, null);

        _ = GetWindowThreadProcessId(windowHandle, out var processId);
        if (processId == 0 || processId == Environment.ProcessId || processId > int.MaxValue)
            return (windowHandle, null);

        try
        {
            using var process = Process.GetProcessById((int)processId);
            return (windowHandle, process.ProcessName);
        }
        catch (Exception exception) when (
            exception is ArgumentException or InvalidOperationException or
            Win32Exception or SecurityException)
        {
            // The foreground process can exit or become inaccessible between
            // reading the window handle and resolving its process information.
            return (windowHandle, null);
        }
    }
}
