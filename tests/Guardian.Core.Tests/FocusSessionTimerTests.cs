using Guardian.Core.Services;

namespace Guardian.Core.Tests;

public sealed class FocusSessionTimerTests
{
    [Fact]
    public void PauseDoesNotConsumeRemainingTimeAndResumeContinues()
    {
        var clock = new ManualTimeProvider();
        var timer = new FocusSessionTimer(clock);

        timer.Start(TimeSpan.FromMinutes(25));
        clock.Advance(TimeSpan.FromMinutes(5));
        Assert.Equal(TimeSpan.FromMinutes(20), timer.Remaining);

        timer.Pause();
        clock.Advance(TimeSpan.FromMinutes(10));
        Assert.Equal(TimeSpan.FromMinutes(20), timer.Remaining);

        timer.Resume();
        clock.Advance(TimeSpan.FromMinutes(2));
        var session = timer.Stop();

        Assert.NotNull(session);
        Assert.Equal(7, session.Minutes, precision: 2);
        Assert.False(session.Completed);
        Assert.Equal("Stopped", session.Outcome);
    }

    [Fact]
    public void CompletedSessionRecordsTheFullPlannedDuration()
    {
        var clock = new ManualTimeProvider();
        var timer = new FocusSessionTimer(clock);

        timer.Start(TimeSpan.FromMinutes(15));
        clock.Advance(TimeSpan.FromMinutes(15));

        var session = timer.Stop(completed: true);

        Assert.NotNull(session);
        Assert.Equal(15, session.Minutes, precision: 2);
        Assert.True(session.Completed);
        Assert.Equal("Completed", session.Outcome);
    }

    [Fact]
    public void RejectsUnreasonableDurations()
    {
        var timer = new FocusSessionTimer(new ManualTimeProvider());

        Assert.Throws<ArgumentOutOfRangeException>(() => timer.Start(TimeSpan.FromSeconds(30)));
        Assert.Throws<ArgumentOutOfRangeException>(() => timer.Start(TimeSpan.FromHours(4)));
    }

    private sealed class ManualTimeProvider : TimeProvider
    {
        private long _timestamp;
        private DateTimeOffset _utcNow = new(2026, 1, 1, 12, 0, 0, TimeSpan.Zero);

        public override long TimestampFrequency => TimeSpan.TicksPerSecond;
        public override long GetTimestamp() => _timestamp;
        public override DateTimeOffset GetUtcNow() => _utcNow;

        public void Advance(TimeSpan elapsed)
        {
            _timestamp += elapsed.Ticks;
            _utcNow += elapsed;
        }
    }
}
