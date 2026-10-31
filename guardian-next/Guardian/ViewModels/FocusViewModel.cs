using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Guardian.Core;
using Guardian.Models;

namespace Guardian.ViewModels
{
    public partial class FocusViewModel : ObservableObject
    {
        private readonly IFocusManager _focusManager;
        private readonly IRepository _repository;
        private FocusSession? _currentSession;

        [ObservableProperty]
        private string _timerDisplay = "25:00";

        [ObservableProperty]
        private int _selectedMinutes = 25;

        [ObservableProperty]
        private bool _isRunning;

        [ObservableProperty]
        private bool _isPaused;

        [ObservableProperty]
        private ObservableCollection<FocusSession> _recentSessions = new();

        public FocusViewModel(IFocusManager focusManager, IRepository repository)
        {
            _focusManager = focusManager;
            _repository = repository;

            _focusManager.TimerUpdated += OnTimerUpdated;
            _focusManager.SessionCompleted += OnSessionCompleted;
        }

        private void OnTimerUpdated(object? sender, TimeSpan remaining)
        {
            System.Windows.Application.Current.Dispatcher.Invoke(() =>
            {
                TimerDisplay = $"{(int)remaining.TotalMinutes:00}:{remaining.Seconds:00}";
            });
        }

        private async void OnSessionCompleted(object? sender, EventArgs e)
        {
            System.Windows.Application.Current.Dispatcher.Invoke(() =>
            {
                IsRunning = false;
                IsPaused = false;
                TimerDisplay = $"{SelectedMinutes:00}:00";
            });

            if (_currentSession != null)
            {
                _currentSession.EndTime = DateTime.Now;
                _currentSession.IsCompleted = true;
                _currentSession.Duration = TimeSpan.FromMinutes(SelectedMinutes);
                await _repository.SaveFocusSessionAsync(_currentSession);
                await LoadRecentSessionsAsync();
            }
        }

        [RelayCommand]
        private async Task StartFocusAsync()
        {
            if (!IsRunning)
            {
                _currentSession = new FocusSession
                {
                    StartTime = DateTime.Now,
                    IsCompleted = false,
                    Duration = TimeSpan.Zero
                };
                await _repository.SaveFocusSessionAsync(_currentSession);

                _focusManager.StartSession(TimeSpan.FromMinutes(SelectedMinutes));
                IsRunning = true;
                IsPaused = false;
            }
        }

        [RelayCommand]
        private void PauseResumeFocus()
        {
            if (IsRunning)
            {
                if (IsPaused)
                {
                    _focusManager.ResumeSession();
                    IsPaused = false;
                }
                else
                {
                    _focusManager.PauseSession();
                    IsPaused = true;
                }
            }
        }

        [RelayCommand]
        private async Task StopFocusAsync()
        {
            if (IsRunning)
            {
                _focusManager.StopSession();
                IsRunning = false;
                IsPaused = false;
                TimerDisplay = $"{SelectedMinutes:00}:00";

                if (_currentSession != null)
                {
                    _currentSession.EndTime = DateTime.Now;
                    _currentSession.Duration = DateTime.Now - _currentSession.StartTime;
                    await _repository.SaveFocusSessionAsync(_currentSession);
                    await LoadRecentSessionsAsync();
                }
            }
        }

        [RelayCommand]
        public async Task LoadRecentSessionsAsync()
        {
            var sessions = await _repository.GetFocusSessionsAsync();
            System.Windows.Application.Current.Dispatcher.Invoke(() =>
            {
                RecentSessions.Clear();
                foreach (var session in sessions) // In real app, reverse and take top N
                {
                    RecentSessions.Insert(0, session);
                }
            });
        }
    }
}
