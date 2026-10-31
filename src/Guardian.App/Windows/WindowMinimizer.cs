using System.Runtime.InteropServices;

namespace Guardian.App.Windows;

internal static class WindowMinimizer
{
    private const int MinimizeCommand = 6;

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool ShowWindowAsync(IntPtr windowHandle, int command);

    public static bool TryMinimize(IntPtr windowHandle) =>
        windowHandle != IntPtr.Zero && ShowWindowAsync(windowHandle, MinimizeCommand);
}
