using System.Windows;
using System.Windows.Controls;
using Guardian.Core.Models;

namespace Guardian.App;

public partial class MainWindow : Window
{
    private readonly GuardianEngine _engine = new();
    private bool _closing;

    public MainWindow()
    {
        InitializeComponent();
        _engine.Changed += RefreshDashboard;
        _engine.FocusChanged += RefreshFocus;
    }

    private async void Window_Loaded(object sender, RoutedEventArgs e)
    {
        await _engine.InitializeAsync();

        MonitoringCheck.IsChecked = _engine.TrackingEnabled;
        BlockingCheck.IsChecked = _engine.BlockingEnabled;
        RefreshDashboard();
        RefreshFocus();
        RefreshBlocks();
        RefreshSessions();

        if (_engine.LoadWarning is not null)
            MessageBox.Show(_engine.LoadWarning, "Guardian data recovery", MessageBoxButton.OK, MessageBoxImage.Warning);
    }

    private async void Window_Closing(object? sender, System.ComponentModel.CancelEventArgs e)
    {
        if (_closing)
            return;

        e.Cancel = true;
        _closing = true;
        await _engine.DisposeAsync();
        Closing -= Window_Closing;
        Close();
    }

    private void ShowPage(string page)
    {
        OverviewPanel.Visibility = page == "overview" ? Visibility.Visible : Visibility.Collapsed;
        FocusPanel.Visibility = page == "focus" ? Visibility.Visible : Visibility.Collapsed;
        BlockingPanel.Visibility = page == "blocking" ? Visibility.Visible : Visibility.Collapsed;
        PrivacyPanel.Visibility = page == "privacy" ? Visibility.Visible : Visibility.Collapsed;
        PageTitle.Text = page switch
        {
            "focus" => "Focus sessions",
            "blocking" => "App blocking",
            "privacy" => "Privacy & data",
            _ => "Overview"
        };
        PageEyebrow.Text = page switch
        {
            "focus" => "MAKE SPACE FOR DEEP WORK",
            "blocking" => "CHOOSE YOUR DISTRACTIONS",
            "privacy" => "YOUR DEVICE, YOUR DATA",
            _ => "YOUR DAY, WITH INTENTION"
        };
        PageSubtitle.Text = page switch
        {
            "focus" => "A simple timer to help you stay with one task.",
            "blocking" => "Gentle, reversible limits for distracting apps.",
            "privacy" => "Transparent controls. Local storage. No telemetry.",
            _ => "A clear picture of where your attention goes."
        };
    }

    private void Overview_Click(object sender, RoutedEventArgs e) => ShowPage("overview");

    private void Focus_Click(object sender, RoutedEventArgs e)
    {
        ShowPage("focus");
        RefreshFocus();
        RefreshSessions();
    }

    private void Blocking_Click(object sender, RoutedEventArgs e)
    {
        ShowPage("blocking");
        RefreshBlocks();
    }

    private void Privacy_Click(object sender, RoutedEventArgs e) => ShowPage("privacy");

    private void StartFocus_Click(object sender, RoutedEventArgs e)
    {
        ShowPage("focus");
        StartTimer_Click(sender, e);
    }

    private int SelectedMinutes() =>
        (DurationBox.SelectedItem as ComboBoxItem)?.Tag is string value &&
        int.TryParse(value, out var minutes) ? minutes : 25;

    private void StartTimer_Click(object sender, RoutedEventArgs e)
    {
        if (_engine.FocusRunning)
            return;

        _engine.StartFocus(SelectedMinutes());
        RefreshFocus();
    }

    private void PauseTimer_Click(object sender, RoutedEventArgs e)
    {
        _engine.PauseResumeFocus();
        RefreshFocus();
    }

    private void StopTimer_Click(object sender, RoutedEventArgs e)
    {
        _engine.StopFocus();
        RefreshFocus();
        RefreshSessions();
    }

    private void RefreshFocus()
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.BeginInvoke(new Action(RefreshFocus));
            return;
        }

        var remaining = _engine.FocusRemaining;
        TimerText.Text = $"{(int)remaining.TotalMinutes:00}:{remaining.Seconds:00}";
        TimerStatus.Text = !_engine.FocusRunning
            ? "Ready when you are."
            : _engine.FocusPaused
                ? "Paused. Take your time."
                : "You're in a focus session. Keep going.";

        StartTimerButton.IsEnabled = !_engine.FocusRunning;
        PauseTimerButton.IsEnabled = _engine.FocusRunning;
        PauseTimerButton.Content = _engine.FocusPaused ? "Resume" : "Pause";
        DurationBox.IsEnabled = !_engine.FocusRunning;
        RefreshSessions();
    }

    private void RefreshDashboard()
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.BeginInvoke(new Action(RefreshDashboard));
            return;
        }

        UsageValue.Text = FormatDuration(_engine.TotalUsageToday);
        FocusValue.Text = $"{(int)_engine.FocusMinutesToday}m";

        var items = _engine.TodayUsage.ToList();
        AppsValue.Text = _engine.Data.Usage
            .Where(item => item.Date == DateTime.Now.ToString("yyyy-MM-dd"))
            .Select(item => item.Name)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .Count()
            .ToString();

        var max = Math.Max(1, items.Count == 0 ? 1 : items.Max(item => item.Seconds));
        foreach (var item in items)
            item.Percent = item.Seconds / max * 100;

        UsageList.ItemsSource = items;
        NoUsageText.Visibility = items.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
        RefreshBlocks();

        if (_engine.PersistenceError is not null)
            PersistenceStatus.Text = _engine.PersistenceError;
        else
            PersistenceStatus.Text = "All data is stored locally on this PC.";
    }

    private static string FormatDuration(double seconds) =>
        seconds >= 3600
            ? $"{(int)(seconds / 3600)}h {((int)(seconds % 3600)) / 60}m"
            : seconds >= 60 ? $"{(int)(seconds / 60)}m" : seconds > 0 ? "<1m" : "0m";

    private void RefreshBlocks()
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.BeginInvoke(new Action(RefreshBlocks));
            return;
        }

        BlockList.ItemsSource = _engine.Data.Blocked.ToList();
        NoBlocksText.Visibility = _engine.Data.Blocked.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
    }

    private void AddBlock_Click(object sender, RoutedEventArgs e)
    {
        var name = BlockNameBox.Text.Trim();
        if (name.Length == 0)
            return;

        if (!_engine.AddBlocked(name))
        {
            BlockErrorText.Text = "Enter a process name such as Discord or chrome.exe. Windows-critical apps cannot be blocked.";
            BlockErrorText.Visibility = Visibility.Visible;
            return;
        }

        BlockErrorText.Visibility = Visibility.Collapsed;
        BlockNameBox.Clear();
        RefreshBlocks();
    }

    private void RemoveBlock_Click(object sender, RoutedEventArgs e)
    {
        if ((sender as Button)?.Tag is string name)
            _engine.RemoveBlocked(name);

        RefreshBlocks();
    }

    private void RefreshSessions()
    {
        if (!Dispatcher.CheckAccess())
        {
            Dispatcher.BeginInvoke(new Action(RefreshSessions));
            return;
        }

        SessionList.ItemsSource = _engine.Data.Sessions.Take(8).Select(session => session.Display).ToList();
    }

    private void Monitoring_Changed(object sender, RoutedEventArgs e)
    {
        if (MonitoringCheck is not null)
            _engine.TrackingEnabled = MonitoringCheck.IsChecked == true;
    }

    private void Blocking_Changed(object sender, RoutedEventArgs e)
    {
        if (BlockingCheck is not null)
            _engine.BlockingEnabled = BlockingCheck.IsChecked == true;
    }

    private void ClearHistory_Click(object sender, RoutedEventArgs e)
    {
        var result = MessageBox.Show(
            "Delete all tracked activity and focus history? This cannot be undone.",
            "Delete local history",
            MessageBoxButton.YesNo,
            MessageBoxImage.Warning);

        if (result == MessageBoxResult.Yes)
        {
            _engine.ClearHistory();
            RefreshDashboard();
            RefreshSessions();
        }
    }
}
