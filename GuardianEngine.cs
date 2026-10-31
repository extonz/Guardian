using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Windows.Threading;

namespace Guardian;

public sealed class GuardianEngine : IDisposable
{
    [DllImport("user32.dll")] private static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", CharSet = CharSet.Unicode)] private static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    [DllImport("user32.dll")] private static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll")] private static extern bool ShowWindow(IntPtr hWnd, int command);
    private const int SW_MINIMIZE = 6;
    private static readonly HashSet<string> ProtectedApps = new(StringComparer.OrdinalIgnoreCase)
    { "guardian", "explorer", "dwm", "csrss", "winlogon", "services", "lsass", "smss", "svchost", "taskmgr", "sihost", "system", "applicationframehost", "shellexperiencehost", "startmenuexperiencehost" };
    private readonly DispatcherTimer _poll = new() { Interval = TimeSpan.FromSeconds(1) };
    private readonly DispatcherTimer _focusTick = new() { Interval = TimeSpan.FromSeconds(1) };
    private readonly string _file;
    private readonly JsonSerializerOptions _json = new() { WriteIndented = true };
    private DateTime _lastTick = DateTime.Now;
    private string? _lastProcess;
    private DateTime _lastProcessStart;
    private bool _tracking = true, _blocking = true, _paused;
    private DateTime _focusEnds;
    private TimeSpan _pausedRemaining;
    public State Data { get; private set; }
    public bool FocusRunning { get; private set; }
    public bool FocusPaused => _paused;
    public TimeSpan FocusRemaining => FocusRunning ? (_paused ? _pausedRemaining : MaxZero(_focusEnds - DateTime.Now)) : TimeSpan.Zero;
    public event Action? Changed;
    public event Action? FocusChanged;
    public GuardianEngine()
    {
        var folder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Guardian");
        Directory.CreateDirectory(folder);
        _file = Path.Combine(folder, "guardian-state.json");
        try { Data = File.Exists(_file) ? JsonSerializer.Deserialize<State>(File.ReadAllText(_file)) ?? new State() : new State(); }
        catch { Data = new State(); }
        _poll.Tick += (_, _) => Tick();
        _focusTick.Tick += (_, _) => FocusTick();
        _poll.Start();
    }
    private static TimeSpan MaxZero(TimeSpan t) => t < TimeSpan.Zero ? TimeSpan.Zero : t;
    public bool TrackingEnabled { get => _tracking; set { _tracking = value; Changed?.Invoke(); } }
    public bool BlockingEnabled { get => _blocking; set { _blocking = value; Changed?.Invoke(); } }
    private void Tick()
    {
        var now = DateTime.Now;
        var elapsed = now - _lastTick;
        _lastTick = now;
        if (elapsed < TimeSpan.Zero || elapsed > TimeSpan.FromSeconds(5)) elapsed = TimeSpan.FromSeconds(1);
        try
        {
            var hwnd = GetForegroundWindow();
            if (hwnd == IntPtr.Zero) return;
            GetWindowThreadProcessId(hwnd, out var pid);
            if (pid == 0 || pid == Environment.ProcessId) return;
            using var process = Process.GetProcessById((int)pid);
            var name = process.ProcessName;
            if (string.IsNullOrWhiteSpace(name) || name.Equals("Idle", StringComparison.OrdinalIgnoreCase)) return;
            if (BlockingEnabled && !ProtectedApps.Contains(name) && Data.Blocked.Contains(name, StringComparer.OrdinalIgnoreCase))
                ShowWindow(hwnd, SW_MINIMIZE);
            if (_tracking)
            {
                var day = now.ToString("yyyy-MM-dd");
                var entry = Data.Usage.FirstOrDefault(x => x.Date == day && x.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
                if (entry == null) { entry = new UsageEntry { Date = day, Name = name }; Data.Usage.Add(entry); }
                entry.Seconds += Math.Clamp(elapsed.TotalSeconds, 0, 2);
                Save();
            }
            Changed?.Invoke();
        }
        catch (Exception ex) when (ex is ArgumentException or InvalidOperationException or System.ComponentModel.Win32Exception or OverflowException) { }
    }
    public void StartFocus(int minutes)
    {
        minutes = Math.Clamp(minutes, 1, 180);
        FocusRunning = true; _paused = false; _focusEnds = DateTime.Now.AddMinutes(minutes);
        Data.ActiveFocusStarted = DateTime.Now; Data.ActiveFocusMinutes = minutes;
        _focusTick.Start(); FocusChanged?.Invoke(); Save();
    }
    public void PauseResumeFocus()
    {
        if (!FocusRunning) return;
        if (!_paused) { _pausedRemaining = MaxZero(_focusEnds - DateTime.Now); _paused = true; _focusTick.Stop(); }
        else { _focusEnds = DateTime.Now + _pausedRemaining; _paused = false; _focusTick.Start(); }
        FocusChanged?.Invoke();
    }
    public void StopFocus(bool completed = false)
    {
        if (!FocusRunning) return;
        var total = Data.ActiveFocusMinutes;
        var remaining = FocusRemaining.TotalMinutes;
        var elapsed = Math.Clamp(total - remaining, 0, total);
        if (completed) elapsed = total;
        if (elapsed > 0.05) Data.Sessions.Insert(0, new SessionEntry { Date = DateTime.Now, Minutes = elapsed, Completed = completed });
        FocusRunning = false; _paused = false; _focusTick.Stop(); Data.ActiveFocusStarted = null; Data.ActiveFocusMinutes = 0;
        Save(); FocusChanged?.Invoke(); Changed?.Invoke();
    }
    private void FocusTick()
    {
        FocusChanged?.Invoke();
        if (FocusRemaining <= TimeSpan.Zero) StopFocus(true);
    }
    public void AddBlocked(string processName)
    {
        var n = Normalize(processName);
        if (n.Length == 0 || ProtectedApps.Contains(n)) return;
        if (!Data.Blocked.Contains(n, StringComparer.OrdinalIgnoreCase)) Data.Blocked.Add(n);
        Save(); Changed?.Invoke();
    }
    public void RemoveBlocked(string processName) { Data.Blocked.RemoveAll(x => x.Equals(processName, StringComparison.OrdinalIgnoreCase)); Save(); Changed?.Invoke(); }
    private static string Normalize(string s) { s = Path.GetFileName((s ?? "").Trim()); return s.EndsWith(".exe", StringComparison.OrdinalIgnoreCase) ? s[..^4] : s; }
    public double TotalUsageToday => Data.Usage.Where(x => x.Date == DateTime.Now.ToString("yyyy-MM-dd")).Sum(x => x.Seconds);
    public double FocusMinutesToday => Data.Sessions.Where(x => x.Date.Date == DateTime.Today).Sum(x => x.Minutes);
    public IEnumerable<UsageEntry> TodayUsage => Data.Usage.Where(x => x.Date == DateTime.Now.ToString("yyyy-MM-dd")).OrderByDescending(x => x.Seconds).Take(12);
    public void ClearHistory() { Data.Usage.Clear(); Data.Sessions.Clear(); Save(); Changed?.Invoke(); }
    private void Save()
    {
        try { File.WriteAllText(_file, JsonSerializer.Serialize(Data, _json)); }
        catch (IOException) { }
        catch (UnauthorizedAccessException) { }
    }
    public void Dispose() { _poll.Stop(); _focusTick.Stop(); Save(); }
}
public sealed class State
{
    public List<UsageEntry> Usage { get; set; } = new();
    public List<SessionEntry> Sessions { get; set; } = new();
    public List<string> Blocked { get; set; } = new();
    public DateTime? ActiveFocusStarted { get; set; }
    public int ActiveFocusMinutes { get; set; }
}
public sealed class UsageEntry { public string Date { get; set; } = ""; public string Name { get; set; } = ""; public double Seconds { get; set; } public string Display => Seconds >= 3600 ? $"{(int)(Seconds/3600)}h {((int)(Seconds%3600))/60}m" : $"{(int)(Seconds/60)}m"; public double Percent { get; set; } }
public sealed class SessionEntry { public DateTime Date { get; set; } public double Minutes { get; set; } public bool Completed { get; set; } public string Display => $"{Date:ddd, HH:mm} · {Minutes:0} min · {(Completed ? "Completed" : "Ended early")}"; }
