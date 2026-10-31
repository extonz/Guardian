using System;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Guardian.Core;
using Guardian.Data;
using Guardian.Services;
using Guardian.ViewModels;

namespace Guardian
{
    public partial class App : Application
    {
        private readonly IHost _host;
        private bool _monitoringStarted;
        public App()
        {
            _host = Host.CreateDefaultBuilder()
                .ConfigureServices((_, services) =>
                {
                    services.AddSingleton<IRepository, SqliteRepository>();
                    services.AddSingleton<IActiveWindowMonitor, ActiveWindowMonitor>();
                    services.AddSingleton<IAppBlocker, AppBlocker>();
                    services.AddSingleton<IFocusManager, FocusManager>();
                    services.AddSingleton<AppUsageTracker>();
                    services.AddSingleton<DashboardViewModel>();
                    services.AddSingleton<FocusViewModel>();
                    services.AddSingleton<BlockingViewModel>();
                    services.AddSingleton<SettingsViewModel>();
                    services.AddSingleton<MainViewModel>();
                    services.AddTransient<MainWindow>();
                }).Build();
        }
        private async void OnStartup(object sender, StartupEventArgs e)
        {
            try
            {
                await _host.StartAsync();
                var repository = _host.Services.GetRequiredService<IRepository>();
                await repository.InitializeAsync();
                var blocker = _host.Services.GetRequiredService<IAppBlocker>();
                foreach (var rule in await repository.GetBlockRulesAsync()) blocker.AddRule(rule);
                var monitor = _host.Services.GetRequiredService<IActiveWindowMonitor>();
                _host.Services.GetRequiredService<AppUsageTracker>().Start();
                blocker.Start();
                monitor.StartMonitoring();
                _monitoringStarted = true;
                MainWindow = _host.Services.GetRequiredService<MainWindow>();
                MainWindow.Show();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Guardian could not start: " + ex.Message,
                    "Guardian startup error", MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(1);
            }
        }
        protected override void OnExit(ExitEventArgs e)
        {
            if (_monitoringStarted)
            {
                _host.Services.GetRequiredService<IActiveWindowMonitor>().StopMonitoring();
                _host.Services.GetRequiredService<IAppBlocker>().Stop();
                _host.Services.GetRequiredService<AppUsageTracker>().Stop();
            }
            _host.StopAsync(TimeSpan.FromSeconds(5)).GetAwaiter().GetResult();
            _host.Dispose();
            base.OnExit(e);
        }
    }
}