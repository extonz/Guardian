using Guardian.Core.Models;

namespace Guardian.Core.Services;

/// <summary>
/// A monotonic focus countdown. It does not depend on the system wall clock,
/// so changing the PC date/time cannot unexpectedly extend or end a session.
/// </summary>
public sealed class FocusSessionTimer
{
    private readonly TimeProvider _timeProvider;
    private long _startedTimestamp;
    private TimeSpan _remainingAtStart;
    private TimeSpan _pausedRemaining;
    private TimeSpan _plannedDuration;
    private DateTimeOffset _sessionStartedAt;

    public FocusSessionTimer(TimeProvider? timeProvider = null)
    {
        _timeProvider = timeProvider ?? TimeProvider.System;
    }

    public bool IsRunning { get; private set; }
    public bool IsPaused { get; private set; }

    public TimeSpan Remaining
    {
        get
        {
            if (!IsRunning)
                return TimeSpan.Zero;

            var remaining = IsPaused
                ? _pausedRemaining
                : _remainingAtStart - _timeProvider.GetElapsedTime(_startedTimestamp);

            return remaining > TimeSpan.Zero ? remaining : TimeSpan.Zero;
        }
    }

    public void Start(TimeSpan duration)
    {
        if (IsRunning)
            throw new InvalidOperationException("A focus session is already running.");
        if (duration < TimeSpan.FromMinutes(1) || duration > TimeSpan.FromHours(3))
            throw new ArgumentOutOfRangeException(nameof(duration), "Focus sessions must be between 1 minute and 3 hours.");

        _sessionStartedAt = _timeProvider.GetUtcNow();
        _plannedDuration = duration;
        _remainingAtStart = duration;
        _pausedRemaining = TimeSpan.Zero;
        _startedTimestamp = _timeProvider.GetTimestamp();
        IsRunning = true;
        IsPaused = false;
    }

    public void Pause()
    {
        if (!IsRunning || IsPaused)
            return;

        _pausedRemaining = Remaining;
        IsPaused = true;
    }

    public void Resume()
    {
        if (!IsRunning || !IsPaused)
            return;

        _remainingAtStart = _pausedRemaining;
        _startedTimestamp = _timeProvider.GetTimestamp();
        _pausedRemaining = TimeSpan.Zero;
        IsPaused = false;
    }

    public SessionEntry? Stop(bool completed = false, bool interrupted = false)
    {
        if (!IsRunning)
            return null;

        var elapsed = _plannedDuration - Remaining;
        if (completed)
            elapsed = _plannedDuration;

        SessionEntry? result = elapsed >= TimeSpan.FromSeconds(1)
            ? new SessionEntry
            {
                Date = _sessionStartedAt,
                Minutes = Math.Round(elapsed.TotalMinutes, 2),
                Completed = completed,
                Outcome = interrupted ? "Interrupted" : completed ? "Completed" : "Stopped"
            }
            : null;

        IsRunning = false;
        IsPaused = false;
        _remainingAtStart = TimeSpan.Zero;
        _pausedRemaining = TimeSpan.Zero;
        _plannedDuration = TimeSpan.Zero;
        return result;
    }
}
