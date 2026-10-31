using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace Guardian;

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
    private void Window_Loaded(object sender, RoutedEventArgs e)
    {
        MonitoringCheck.IsChecked = _engine.TrackingEnabled;
        BlockingCheck.IsChecked = _engine.BlockingEnabled;
        RefreshDashboard(); RefreshFocus(); RefreshBlocks(); RefreshSessions();
    }
    private void Window_Closing(object? sender, System.ComponentModel.CancelEventArgs e)
    {
        if (_closing) return;
        _closing = true; _engine.Dispose();
    }
    private void ShowPage(string page)
    {
        OverviewPanel.Visibility = page == "overview" ? Visibility.Visible : Visibility.Collapsed;
        FocusPanel.Visibility = page == "focus" ? Visibility.Visible : Visibility.Collapsed;
        BlockingPanel.Visibility = page == "blocking" ? Visibility.Visible : Visibility.Collapsed;
        PrivacyPanel.Visibility = page == "privacy" ? Visibility.Visible : Visibility.Collapsed;
        PageTitle.Text = page switch { "focus" => "Focus sessions", "blocking" => "App blocking", "privacy" => "Privacy & data", _ => "Overview" };
        PageEyebrow.Text = page switch { "focus" => "MAKE SPACE FOR DEEP WORK", "blocking" => "CHOOSE YOUR DISTRACTIONS", "privacy" => "YOUR DEVICE, YOUR DATA", _ => "YOUR DAY, WITH INTENTION" };
        PageSubtitle.Text = page switch { "focus" => "A simple timer to help you stay with one task.", "blocking" => "Gentle, reversible limits for distracting apps.", "privacy" => "Transparent controls. Local storage. No telemetry.", _ => "A clear picture of where your attention goes." };
    }
    private void Overview_Click(object sender, RoutedEventArgs e) => ShowPage("overview");
    private void Focus_Click(object sender, RoutedEventArgs e) { ShowPage("focus"); RefreshFocus(); RefreshSessions(); }
    private void Blocking_Click(object sender, RoutedEventArgs e) { ShowPage("blocking"); RefreshBlocks(); }
    private void Privacy_Click(object sender, RoutedEventArgs e) => ShowPage("privacy");
    private void StartFocus_Click(object sender, RoutedEventArgs e) { ShowPage("focus"); StartTimer_Click(sender, e); }
    private int SelectedMinutes() => (DurationBox.SelectedItem as ComboBoxItem)?.Tag is string s && int.TryParse(s, out var m) ? m : 25;
    private void StartTimer_Click(object sender, RoutedEventArgs e)
    {
        if (_engine.FocusRunning) return;
        _engine.StartFocus(SelectedMinutes()); RefreshFocus();
    }
    private void PauseTimer_Click(object sender, RoutedEventArgs e) { _engine.PauseResumeFocus(); RefreshFocus(); }
    private void StopTimer_Click(object sender, RoutedEventArgs e) { _engine.StopFocus(); RefreshFocus(); RefreshSessions(); }
    private void RefreshFocus()
    {
        Dispatcher.Invoke(() =>
        {
            var t = _engine.FocusRemaining;
            TimerText.Text = $"{(int)t.TotalMinutes:00}:{t.Seconds:00}";
            TimerStatus.Text = !_engine.FocusRunning ? "Ready when you are." : _engine.FocusPaused ? "Paused. Take your time." : "You're in a focus session. Keep going.";
            StartTimerButton.IsEnabled = !_engine.FocusRunning;
            PauseTimerButton.IsEnabled = _engine.FocusRunning;
            PauseTimerButton.Content = _engine.FocusPaused ? "Resume" : "Pause";
            DurationBox.IsEnabled = !_engine.FocusRunning;
            RefreshSessions();
        });
    }
    private void RefreshDashboard()
    {
        if (!Dispatcher.CheckAccess()) { Dispatcher.BeginInvoke(RefreshDashboard); return; }
        UsageValue.Text = FormatDuration(_engine.TotalUsageToday);
        FocusValue.Text = $"{(int)_engine.FocusMinutesToday}m";
        var items = _engine.TodayUsage.ToList();
        AppsValue.Text = items.Count.ToString();
        var max = Math.Max(1, items.Count == 0 ? 1 : items.Max(x => x.Seconds));
        foreach (var item in items) item.Percent = item.Seconds / max * 100;
        UsageList.ItemsSource = items;
        NoUsageText.Visibility = items.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
        RefreshBlocks();
    }
    private static string FormatDuration(double seconds) => seconds >= 3600 ? $"{(int)(seconds/3600)}h {((int)(seconds%3600))/60}m" : $"{(int)(seconds/60)}m";
    private void RefreshBlocks()
    {
        if (!Dispatcher.CheckAccess()) { Dispatcher.BeginInvoke(RefreshBlocks); return; }
        BlockList.ItemsSource = _engine.Data.Blocked.ToList();
        NoBlocksText.Visibility = _engine.Data.Blocked.Count == 0 ? Visibility.Visible : Visibility.Collapsed;
    }
    private void AddBlock_Click(object sender, RoutedEventArgs e)
    {
        var name = BlockNameBox.Text.Trim();
        if (name.Length == 0) return;
        _engine.AddBlocked(name); BlockNameBox.Clear(); RefreshBlocks();
    }
    private void RemoveBlock_Click(object sender, RoutedEventArgs e)
    {
        if ((sender as Button)?.Tag is string name) _engine.RemoveBlocked(name);
        RefreshBlocks();
    }
    private void RefreshSessions()
    {
        if (!Dispatcher.CheckAccess()) { Dispatcher.BeginInvoke(RefreshSessions); return; }
        SessionList.ItemsSource = _engine.Data.Sessions.Take(8).Select(x => x.Display).ToList();
    }
    private void Monitoring_Changed(object sender, RoutedEventArgs e)
    {
        if (MonitoringCheck == null) return;
        _engine.TrackingEnabled = MonitoringCheck.IsChecked == true;
    }
    private void Blocking_Changed(object sender, RoutedEventArgs e)
    {
        if (BlockingCheck == null) return;
        _engine.BlockingEnabled = BlockingCheck.IsChecked == true;
    }
    private void ClearHistory_Click(object sender, RoutedEventArgs e)
    {
        if (MessageBox.Show("Delete all tracked activity and focus history? This cannot be undone.", "Delete local history", MessageBoxButton.YesNo, MessageBoxImage.Warning) == MessageBoxResult.Yes)
        { _engine.ClearHistory(); RefreshDashboard(); RefreshSessions(); }
    }
}
