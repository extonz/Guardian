using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Guardian.Core;
using Guardian.Services;

namespace Guardian.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        private readonly IRepository _repository;
        private readonly AppUsageTracker _tracker;
        private readonly IAppBlocker _blocker;
        private readonly IActiveWindowMonitor _monitor;

        [ObservableProperty]
        private ObservableObject? _currentViewModel;

        public DashboardViewModel DashboardVM { get; }
        public FocusViewModel FocusVM { get; }
        public BlockingViewModel BlockingVM { get; }
        public SettingsViewModel SettingsVM { get; }

        public MainViewModel(
            IRepository repository,
            AppUsageTracker tracker,
            IAppBlocker blocker,
            IActiveWindowMonitor monitor,
            DashboardViewModel dashboardVM,
            FocusViewModel focusVM,
            BlockingViewModel blockingVM,
            SettingsViewModel settingsVM)
        {
            _repository = repository;
            _tracker = tracker;
            _blocker = blocker;
            _monitor = monitor;

            DashboardVM = dashboardVM;
            FocusVM = focusVM;
            BlockingVM = blockingVM;
            SettingsVM = settingsVM;

            CurrentViewModel = DashboardVM;

            InitializeAsync();
        }

        private async void InitializeAsync()
        {
            await _repository.InitializeAsync();

            var rules = await _repository.GetBlockRulesAsync();
            foreach (var rule in rules)
            {
                if (rule.IsActive)
                {
                    _blocker.AddRule(rule);
                }
            }

            _monitor.StartMonitoring();
            _tracker.Start();
            _blocker.Start();
        }

        [RelayCommand]
        private void NavigateToDashboard() => CurrentViewModel = DashboardVM;

        [RelayCommand]
        private void NavigateToFocus() => CurrentViewModel = FocusVM;

        [RelayCommand]
        private void NavigateToBlocking() => CurrentViewModel = BlockingVM;

        [RelayCommand]
        private void NavigateToSettings() => CurrentViewModel = SettingsVM;
    }
}
