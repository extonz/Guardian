using System;
using System.Threading.Tasks;
using Guardian.Services;
using Xunit;

namespace Guardian.Tests.Services
{
    public class FocusManagerTests
    {
        [Fact]
        public void StartSession_SetsStateCorrectly()
        {
            var manager = new FocusManager();
            var duration = TimeSpan.FromMinutes(25);

            manager.StartSession(duration);

            Assert.True(manager.IsRunning);
            Assert.Equal(duration, manager.RemainingTime);
        }

        [Fact]
        public void PauseSession_SetsIsRunningToFalse()
        {
            var manager = new FocusManager();
            manager.StartSession(TimeSpan.FromMinutes(25));

            manager.PauseSession();

            Assert.False(manager.IsRunning);
        }

        [Fact]
        public void ResumeSession_RestoresIsRunning()
        {
            var manager = new FocusManager();
            manager.StartSession(TimeSpan.FromMinutes(25));
            manager.PauseSession();

            manager.ResumeSession();

            Assert.True(manager.IsRunning);
        }

        [Fact]
        public void StopSession_ClearsRemainingTime()
        {
            var manager = new FocusManager();
            manager.StartSession(TimeSpan.FromMinutes(25));

            manager.StopSession();

            Assert.False(manager.IsRunning);
            Assert.Equal(TimeSpan.Zero, manager.RemainingTime);
        }
    }
}
