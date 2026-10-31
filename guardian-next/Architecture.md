# Architecture Overview

Guardian Next is a modern Windows WPF application utilizing the MVVM architectural pattern.

## Core Layers
1. **Views**: `MainWindow.xaml` holds a sidebar navigation layout. Content is dynamically swapped into the `ContentControl` via DataTemplates bound to specific ViewModels. UserControls (`DashboardView`, `FocusView`, `BlockingView`, `SettingsView`) handle the actual UI.
2. **ViewModels**: Built on `CommunityToolkit.Mvvm`, these act as the bridge. They implement `ObservableObject` and use `[ObservableProperty]` and `[RelayCommand]` attributes via source generators to dramatically reduce boilerplate code.
3. **Core Services**:
   - `ActiveWindowMonitor`: Uses PInvoke (`user32.dll`) to poll `GetForegroundWindow` and retrieve active Window process names and titles.
   - `AppBlocker`: Subscribes to the `ActiveWindowMonitor` and issues a process close command if a blocked application takes foreground.
   - `FocusManager`: Handles countdown timers and session states asynchronously.
   - `AppUsageTracker`: Computes duration between window switches and saves usage spans to the repository.
4. **Data Repository**: `SqliteRepository` handles all storage. Configured to store a single `guardian.db` inside the `%LOCALAPPDATA%\Guardian` directory, keeping things organized and local to the user profile.

## Key Design Choices
- **C# 10 / .NET 10 WPF**: The target framework ensures high performance, access to modern language features (like source generators), and native Windows aesthetic capabilities.
- **Dependency Injection**: `Microsoft.Extensions.Hosting` is used in `App.xaml.cs` to set up the DI container, registering singletons for repositories and ViewModels, ensuring a single state truth across the app lifecycle.
- **Local Only**: No network requests exist in the app logic, adhering strictly to the privacy-first design request.
