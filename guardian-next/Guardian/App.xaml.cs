using System;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Guardian.Core;
using Guardian.Data;
using Guardian.Services;
using Guardian.ViewModels;
using Guardian.Views;

namespace Guardian
{
    public partial class App : Application
    {
        private IHost _host;

        public App()
        {
            _host = Host.CreateDefaultBuilder()
                .ConfigureServices((context, services) =>
                {
                    ConfigureServices(services);
                })
                .Build();
        }

        private void ConfigureServices(IServiceCollection services)
        {
            // Core
            services.AddSingleton<IRepository, SqliteRepository>();
            services.AddSingleton<IActiveWindowMonitor, ActiveWindowMonitor>();
            services.AddSingleton<IAppBlocker, AppBlocker>();
            services.AddSingleton<IFocusManager, FocusManager>();
            services.AddSingleton<AppUsageTracker>();

            // ViewModels
            services.AddSingleton<DashboardViewModel>();
            services.AddSingleton<FocusViewModel>();
            services.AddSingleton<BlockingViewModel>();
            services.AddSingleton<SettingsViewModel>();
            services.AddSingleton<MainViewModel>();

            // Views
            services.AddTransient<MainWindow>();
        }

        private async void OnStartup(object sender, StartupEventArgs e)
        {
            await _host.StartAsync();

            var mainWindow = _host.Services.GetRequiredService<MainWindow>();
            mainWindow.Show();
        }

        protected override async void OnExit(ExitEventArgs e)
        {
            using (_host)
            {
                await _host.StopAsync(TimeSpan.FromSeconds(5));
            }
            base.OnExit(e);
        }
    }
}
