using System.Globalization;
using Guardian.Core.Models;

namespace Guardian.Core.Services;

/// <summary>
/// Attributes the time between two observations to the process that was active
/// at the earlier observation. Long polling gaps are discarded (for example,
/// after sleep or a debugger pause) rather than recorded as app usage.
/// </summary>
public sealed class UsageLedger
{
    private static readonly TimeSpan MaximumSampleGap = TimeSpan.FromSeconds(5);
    private readonly IList<UsageEntry> _entries;
    private DateTimeOffset? _lastObservedAt;
    private string? _activeProcess;

    public UsageLedger(IList<UsageEntry> entries)
    {
        _entries = entries ?? throw new ArgumentNullException(nameof(entries));
    }

    public void Observe(string? processName, DateTimeOffset observedAt)
    {
        var normalized = ProcessNameRules.TryNormalize(processName, out var value) ? value : null;

        if (_lastObservedAt is { } previousAt && observedAt >= previousAt && _activeProcess is not null)
        {
            var elapsed = observedAt - previousAt;
            if (elapsed > TimeSpan.Zero && elapsed <= MaximumSampleGap)
                AddInterval(_activeProcess, previousAt, observedAt);
        }

        // A backwards clock adjustment resets the sampling baseline; it never
        // creates a negative or duplicated usage interval.
        _lastObservedAt = observedAt;
        _activeProcess = normalized;
    }

    public void Reset(DateTimeOffset observedAt)
    {
        _lastObservedAt = observedAt;
        _activeProcess = null;
    }

    private void AddInterval(string processName, DateTimeOffset start, DateTimeOffset end)
    {
        var cursor = start;

        // Split intervals at local midnight so daily totals remain correct.
        while (cursor < end)
        {
            var localCursor = cursor.LocalDateTime;
            var nextMidnight = localCursor.Date.AddDays(1);
            var boundaryOffset = TimeZoneInfo.Local.GetUtcOffset(nextMidnight);
            var boundary = new DateTimeOffset(nextMidnight, boundaryOffset);
            var segmentEnd = boundary > cursor && boundary < end ? boundary : end;

            var date = cursor.LocalDateTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
            AddSeconds(date, processName, (segmentEnd - cursor).TotalSeconds);
            cursor = segmentEnd;
        }
    }

    private void AddSeconds(string date, string processName, double seconds)
    {
        if (seconds <= 0 || !double.IsFinite(seconds))
            return;

        var entry = _entries.FirstOrDefault(item =>
            item.Date == date && item.Name.Equals(processName, StringComparison.OrdinalIgnoreCase));

        if (entry is null)
        {
            entry = new UsageEntry { Date = date, Name = processName };
            _entries.Add(entry);
        }

        entry.Seconds = Math.Round(entry.Seconds + seconds, 2, MidpointRounding.AwayFromZero);
    }
}
