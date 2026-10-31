using System;

namespace Guardian.Core
{
    public interface IFocusManager
    {
        event EventHandler<TimeSpan> TimerUpdated;
        event EventHandler SessionCompleted;

        bool IsRunning { get; }
        TimeSpan RemainingTime { get; }

        void StartSession(TimeSpan duration);
        void PauseSession();
        void ResumeSession();
        void StopSession();
    }
}
