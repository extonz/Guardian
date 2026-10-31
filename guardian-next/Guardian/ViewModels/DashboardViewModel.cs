using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Guardian.Core;

namespace Guardian.ViewModels
{
    public partial class AppUsageDisplay : ObservableObject
    {
        public string ProcessName { get; set; } = string.Empty;
        public TimeSpan TotalDuration { get; set; }
        public string FormattedDuration => $"{(int)TotalDuration.TotalHours}h {TotalDuration.Minutes}m";
    }

    public partial class DashboardViewModel : ObservableObject
    {
        private readonly IRepository _repository;

        [ObservableProperty]
        private ObservableCollection<AppUsageDisplay> _todayUsage = new();

        [ObservableProperty]
        private string _totalTimeToday = "0h 0m";

        public DashboardViewModel(IRepository repository)
        {
            _repository = repository;
        }

        [RelayCommand]
        public async Task LoadDataAsync()
        {
            var usages = await _repository.GetAppUsagesAsync(DateTime.Today);

            var grouped = usages.GroupBy(u => u.ProcessName)
                .Select(g => new AppUsageDisplay
                {
                    ProcessName = g.Key,
                    TotalDuration = TimeSpan.FromSeconds(g.Sum(x => x.Duration.TotalSeconds))
                })
                .OrderByDescending(x => x.TotalDuration)
                .ToList();

            TodayUsage.Clear();
            TimeSpan total = TimeSpan.Zero;

            foreach (var item in grouped)
            {
                TodayUsage.Add(item);
                total += item.TotalDuration;
            }

            TotalTimeToday = $"{(int)total.TotalHours}h {total.Minutes}m";
        }
    }
}
