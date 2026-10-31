using System.Globalization;
using System.Text.Json.Serialization;
using Guardian.Core.Services;

namespace Guardian.Core.Models;

public sealed class GuardianState
{
    public int SchemaVersion { get; set; } = 2;
    public List<UsageEntry> Usage { get; set; } = [];
    public List<SessionEntry> Sessions { get; set; } = [];
    public List<string> Blocked { get; set; } = [];
    public bool TrackingEnabled { get; set; } = true;
    public bool BlockingEnabled { get; set; } = true;

    public void Normalize()
    {
        Usage ??= [];
        Sessions ??= [];
        Blocked ??= [];

        Usage = Usage
            .Where(x => x is not null &&
                        !string.IsNullOrWhiteSpace(x.Name) &&
                        DateOnly.TryParseExact(x.Date, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _) &&
                        double.IsFinite(x.Seconds) && x.Seconds >= 0)
            .GroupBy(x => (x.Date, x.Name), UsageKeyComparer.Instance)
            .Select(group => new UsageEntry
            {
                Date = group.Key.Date,
                Name = group.Key.Name,
                Seconds = group.Sum(x => x.Seconds)
            })
            .ToList();

        Sessions = Sessions
            .Where(x => x is not null && double.IsFinite(x.Minutes) && x.Minutes > 0)
            .OrderByDescending(x => x.Date)
            .ToList();

        Blocked = Blocked
            .Select(value => ProcessNameRules.TryNormalize(value, out var normalized) ? normalized : null)
            .Where(value => value is not null && !ProcessNameRules.IsProtected(value))
            .Select(value => value!)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .OrderBy(value => value, StringComparer.OrdinalIgnoreCase)
            .ToList();

        SchemaVersion = 2;
    }

    private sealed class UsageKeyComparer : IEqualityComparer<(string Date, string Name)>
    {
        public static readonly UsageKeyComparer Instance = new();
        public bool Equals((string Date, string Name) x, (string Date, string Name) y) =>
            StringComparer.Ordinal.Equals(x.Date, y.Date) &&
            StringComparer.OrdinalIgnoreCase.Equals(x.Name, y.Name);
        public int GetHashCode((string Date, string Name) value) =>
            HashCode.Combine(StringComparer.Ordinal.GetHashCode(value.Date),
                StringComparer.OrdinalIgnoreCase.GetHashCode(value.Name));
    }
}

public sealed class UsageEntry
{
    public string Date { get; set; } = "";
    public string Name { get; set; } = "";
    public double Seconds { get; set; }

    [JsonIgnore]
    public string Display => Seconds >= 3600
        ? $"{(int)(Seconds / 3600)}h {((int)(Seconds % 3600)) / 60}m"
        : Seconds >= 60 ? $"{(int)(Seconds / 60)}m" : Seconds > 0 ? "<1m" : "0m";

    [JsonIgnore]
    public double Percent { get; set; }
}

public sealed class SessionEntry
{
    public DateTimeOffset Date { get; set; }
    public double Minutes { get; set; }
    public bool Completed { get; set; }
    public string Outcome { get; set; } = "Stopped";

    [JsonIgnore]
    public string Display =>
        $"{Date.LocalDateTime:ddd, HH:mm} · {Minutes:0} min · " +
        (Completed ? "Completed" : Outcome == "Interrupted" ? "Interrupted" : "Ended early");
}
