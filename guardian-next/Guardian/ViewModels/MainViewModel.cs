using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace Guardian.ViewModels
{
    public partial class MainViewModel : ObservableObject
    {
        [ObservableProperty] private ObservableObject? _currentViewModel;
        public DashboardViewModel DashboardVM { get; }
        public FocusViewModel FocusVM { get; }
        public BlockingViewModel BlockingVM { get; }
        public SettingsViewModel SettingsVM { get; }
        public MainViewModel(DashboardViewModel dashboardVM, FocusViewModel focusVM,
            BlockingViewModel blockingVM, SettingsViewModel settingsVM)
        {
            DashboardVM = dashboardVM;
            FocusVM = focusVM;
            BlockingVM = blockingVM;
            SettingsVM = settingsVM;
            CurrentViewModel = DashboardVM;
            _ = DashboardVM.LoadDataAsync();
            _ = BlockingVM.LoadRulesAsync();
            _ = FocusVM.LoadRecentSessionsAsync();
        }
        [RelayCommand] private void NavigateToDashboard()
        {
            CurrentViewModel = DashboardVM;
            _ = DashboardVM.LoadDataAsync();
        }
        [RelayCommand] private void NavigateToFocus() => CurrentViewModel = FocusVM;
        [RelayCommand] private void NavigateToBlocking()
        {
            CurrentViewModel = BlockingVM;
            _ = BlockingVM.LoadRulesAsync();
        }
        [RelayCommand] private void NavigateToSettings() => CurrentViewModel = SettingsVM;
    }
}