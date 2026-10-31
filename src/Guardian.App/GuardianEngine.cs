using System.Text.Json;
using System.Windows.Threading;
using Guardian.App.Windows;
using Guardian.Core.Models;
using Guardian.Core.Services;
using Guardian.Core.Storage;

namespace Guardian.App;

public sealed class GuardianEngine : IAsyncDisposable
{
    private static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = true };
    private readonly JsonStateStore _store = new();
    private readonly FocusSessionTimer _focusTimer = new();
    private readonly DispatcherTimer _pollTimer = new() { Interval = TimeSpan.FromSeconds(1) };
    private readonly DispatcherTimer _focusTickTimer = new() { Interval = TimeSpan.FromSeconds(1) };
    private readonly DispatcherTimer _saveTimer = new() { Interval = TimeSpan.FromSeconds(15) };
    private readonly SemaphoreSlim _saveGate = new(1, 1);
    private UsageLedger? _usageLedger;
    private bool _initialized;
    private bool _disposed;

    public GuardianState Data { get; private set; } = new();
    public string? LoadWarning { get; private set; }
    public string? PersistenceError { get; private set; }

    public event Action? Changed;
    public event Action? FocusChanged;

    public bool TrackingEnabled
    {
        get => Data.TrackingEnabled;
        set
        {
            if (Data.TrackingEnabled == value)
                return;

            Data.TrackingEnabled = value;
            _usageLedger?.Reset(DateTimeOffset.Now);
            _ = SaveAsync();
            Changed?.Invoke();
        }
    }

    public bool BlockingEnabled
    {
        get => Data.BlockingEnabled;
        set
        {
            if (Data.BlockingEnabled == value)
                return;

            Data.BlockingEnabled = value;
            _ = SaveAsync();
            Changed?.Invoke();
        }
    }

    public bool FocusRunning => _focusTimer.IsRunning;
    public bool FocusPaused => _focusTimer.IsPaused;
    public TimeSpan FocusRemaining => _focusTimer.Remaining;

    public double TotalUsageToday
    {
        get
        {
            var today = DateTime.Now.ToString("yyyy-MM-dd");
            return Data.Usage.Where(entry => entry.Date == today).Sum(entry => entry.Seconds);
        }
    }

    public double FocusMinutesToday =>
        Data.Sessions.Where(session => session.Date.LocalDateTime.Date == DateTime.Today)
            .Sum(session => session.Minutes);

    public IEnumerable<UsageEntry> TodayUsage
    {
        get
        {
            var today = DateTime.Now.ToString("yyyy-MM-dd");
            return Data.Usage.Where(entry => entry.Date == today)
                .OrderByDescending(entry => entry.Seconds)
                .Take(12);
        }
    }

    public async Task InitializeAsync()
    {
        if (_initialized)
            return;

        var loaded = await _store.LoadAsync();
        Data = loaded.State;
        LoadWarning = loaded.Warning;
        Data.Normalize();
        _usageLedger = new UsageLedger(Data.Usage);

        _pollTimer.Tick += PollTimer_Tick;
        _focusTickTimer.Tick += FocusTickTimer_Tick;
        _saveTimer.Tick += SaveTimer_Tick;
        _pollTimer.Start();
        _saveTimer.Start();
        _initialized = true;
    }

    private void PollTimer_Tick(object? sender, EventArgs e)
    {
        if (_usageLedger is null)
            return;

        var now = DateTimeOffset.Now;
        var active = ForegroundAppMonitor.Read();

        if (TrackingEnabled)
            _usageLedger.Observe(active.ProcessName, now);
        else
            _usageLedger.Reset(now);

        if (BlockingEnabled &&
            active.ProcessName is { } processName &&
            Data.Blocked.Contains(processName, StringComparer.OrdinalIgnoreCase))
        {
            _ = WindowMinimizer.TryMinimize(active.WindowHandle);
        }

        Changed?.Invoke();
    }

    public void StartFocus(int minutes)
    {
        if (!_initialized || FocusRunning)
            return;

        _focusTimer.Start(TimeSpan.FromMinutes(Math.Clamp(minutes, 1, 180)));
        _focusTickTimer.Start();
        FocusChanged?.Invoke();
    }

    public void PauseResumeFocus()
    {
        if (!FocusRunning)
            return;

        if (FocusPaused)
            _focusTimer.Resume();
        else
            _focusTimer.Pause();

        FocusChanged?.Invoke();
    }

    public void StopFocus(bool completed = false, bool interrupted = false)
    {
        var session = _focusTimer.Stop(completed, interrupted);
        _focusTickTimer.Stop();

        if (session is not null)
        {
            Data.Sessions.Insert(0, session);
            Data.Sessions = Data.Sessions.OrderByDescending(item => item.Date).Take(500).ToList();
            _ = SaveAsync();
            Changed?.Invoke();
        }

        FocusChanged?.Invoke();
    }

    private void FocusTickTimer_Tick(object? sender, EventArgs e)
    {
        FocusChanged?.Invoke();
        if (_focusTimer.Remaining <= TimeSpan.Zero)
            StopFocus(completed: true);
    }

    private async void SaveTimer_Tick(object? sender, EventArgs e) =>
        await SaveAsync();

    public bool AddBlocked(string processName)
    {
        if (!ProcessNameRules.TryNormalize(processName, out var normalized) ||
            ProcessNameRules.IsProtected(normalized))
            return false;

        if (!Data.Blocked.Contains(normalized, StringComparer.OrdinalIgnoreCase))
        {
            Data.Blocked.Add(normalized);
            Data.Blocked = Data.Blocked.OrderBy(value => value, StringComparer.OrdinalIgnoreCase).ToList();
            _ = SaveAsync();
            Changed?.Invoke();
        }

        return true;
    }

    public void RemoveBlocked(string processName)
    {
        if (!ProcessNameRules.TryNormalize(processName, out var normalized))
            return;

        Data.Blocked.RemoveAll(value => value.Equals(normalized, StringComparison.OrdinalIgnoreCase));
        _ = SaveAsync();
        Changed?.Invoke();
    }

    public void ClearHistory()
    {
        Data.Usage.Clear();
        Data.Sessions.Clear();
        _ = SaveAsync();
        Changed?.Invoke();
    }

    private async Task SaveAsync(bool finalSave = false)
    {
        if (!_initialized || (_disposed && !finalSave))
            return;

        await _saveGate.WaitAsync();
        try
        {
            // Re-check after acquiring the gate: a queued periodic write must
            // not run after shutdown and overwrite the final state snapshot.
            if (_disposed && !finalSave)
                return;

            var snapshot = JsonSerializer.Serialize(Data, JsonOptions);
            await _store.SaveJsonAsync(snapshot);
            PersistenceError = null;
        }
        catch (Exception exception) when (exception is IOException or UnauthorizedAccessException)
        {
            PersistenceError = $"Guardian could not save local data: {exception.Message}";
        }
        finally
        {
            _saveGate.Release();
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_disposed)
            return;

        _disposed = true;
        _pollTimer.Stop();
        _focusTickTimer.Stop();
        _saveTimer.Stop();

        if (TrackingEnabled)
            _usageLedger?.Observe(null, DateTimeOffset.Now);

        var interruptedSession = _focusTimer.Stop(interrupted: true);
        if (interruptedSession is not null)
            Data.Sessions.Insert(0, interruptedSession);

        await SaveAsync(finalSave: true);
    }
}
