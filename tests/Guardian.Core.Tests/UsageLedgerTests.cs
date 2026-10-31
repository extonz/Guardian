using Guardian.Core.Models;
using Guardian.Core.Services;

namespace Guardian.Core.Tests;

public sealed class UsageLedgerTests
{
    [Fact]
    public void AttributesElapsedTimeToThePreviouslyObservedForegroundApp()
    {
        var entries = new List<UsageEntry>();
        var ledger = new UsageLedger(entries);
        var start = DateTimeOffset.Now;

        ledger.Observe("chrome", start);
        ledger.Observe("discord.exe", start.AddSeconds(1));
        ledger.Observe("discord", start.AddSeconds(2));
        ledger.Observe(null, start.AddSeconds(3));

        Assert.Equal(2, Assert.Single(entries.Where(item => item.Name == "chrome")).Seconds);
        Assert.Equal(1, Assert.Single(entries.Where(item => item.Name == "discord")).Seconds);
    }

    [Fact]
    public void SplitsUsageAcrossLocalMidnight()
    {
        var entries = new List<UsageEntry>();
        var ledger = new UsageLedger(entries);
        var localStart = new DateTime(2026, 10, 30, 23, 59, 59, DateTimeKind.Local);
        var start = new DateTimeOffset(localStart);

        ledger.Observe("browser", start);
        ledger.Observe("browser", start.AddSeconds(1));
        ledger.Observe(null, start.AddSeconds(2));

        Assert.Equal(1, Assert.Single(entries.Where(item => item.Date == "2026-10-30")).Seconds);
        Assert.Equal(1, Assert.Single(entries.Where(item => item.Date == "2026-10-31")).Seconds);
    }

    [Fact]
    public void DiscardsLongGapsInsteadOfCountingSleepAsUsage()
    {
        var entries = new List<UsageEntry>();
        var ledger = new UsageLedger(entries);
        var start = DateTimeOffset.Now;

        ledger.Observe("chrome", start);
        ledger.Observe("chrome", start.AddSeconds(45));

        Assert.Empty(entries);
    }

    [Fact]
    public void DoesNotCountTimeWhenNoForegroundProcessIsAvailable()
    {
        var entries = new List<UsageEntry>();
        var ledger = new UsageLedger(entries);
        var start = DateTimeOffset.Now;

        ledger.Observe(null, start);
        ledger.Observe("chrome", start.AddSeconds(1));

        Assert.Empty(entries);
    }
}
