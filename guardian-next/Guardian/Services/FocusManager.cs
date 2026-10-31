using System;
using System.Threading;
using System.Threading.Tasks;
using Guardian.Core;

namespace Guardian.Services
{
    public class FocusManager : IFocusManager
    {
        public event EventHandler<TimeSpan>? TimerUpdated;
        public event EventHandler? SessionCompleted;

        private CancellationTokenSource? _cancellationTokenSource;
        private TimeSpan _remainingTime;
        private bool _isPaused;

        public bool IsRunning => _cancellationTokenSource != null && !_isPaused;
        public TimeSpan RemainingTime => _remainingTime;

        public void StartSession(TimeSpan duration)
        {
            StopSession();

            _remainingTime = duration;
            _isPaused = false;
            _cancellationTokenSource = new CancellationTokenSource();

            TimerUpdated?.Invoke(this, _remainingTime);

            Task.Run(async () => await RunTimerAsync(_cancellationTokenSource.Token));
        }

        public void PauseSession()
        {
            if (_cancellationTokenSource != null)
            {
                _isPaused = true;
            }
        }

        public void ResumeSession()
        {
            if (_cancellationTokenSource != null && _isPaused)
            {
                _isPaused = false;
            }
        }

        public void StopSession()
        {
            _cancellationTokenSource?.Cancel();
            _cancellationTokenSource?.Dispose();
            _cancellationTokenSource = null;
            _isPaused = false;
            _remainingTime = TimeSpan.Zero;
            TimerUpdated?.Invoke(this, _remainingTime);
        }

        private async Task RunTimerAsync(CancellationToken token)
        {
            while (!token.IsCancellationRequested && _remainingTime > TimeSpan.Zero)
            {
                await Task.Delay(1000, token);

                if (!_isPaused && !token.IsCancellationRequested)
                {
                    _remainingTime = _remainingTime.Subtract(TimeSpan.FromSeconds(1));
                    TimerUpdated?.Invoke(this, _remainingTime);

                    if (_remainingTime <= TimeSpan.Zero)
                    {
                        SessionCompleted?.Invoke(this, EventArgs.Empty);
                        _cancellationTokenSource?.Cancel();
                    }
                }
            }
        }
    }
}
