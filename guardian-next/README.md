# Guardian Next

Guardian Next is a complete redesign and rewrite of the Guardian digital wellbeing application, shifting from Python/Tkinter to C# .NET WPF for a native, robust, and modern Windows desktop experience.

## Features
- **Application Monitoring**: Accurately tracks foreground activity and app usage duration locally using native Windows APIs.
- **Application Blocking**: Allows setting block rules for apps and effectively closes them if they attempt to take focus.
- **Focus Mode**: A dedicated timer section with pause/resume functionality to track dedicated work sessions, completely separate from active app tracking.
- **Dashboard Statistics**: A clean, Linear/Raycast-inspired UI that visually breaks down most-used applications and total daily time.
- **Local Persistence**: All data (settings, usage, block rules) is stored locally on-disk via SQLite (`%LOCALAPPDATA%\Guardian\guardian.db`).
- **Privacy First**: No telemetry. No cloud syncing. Completely private.

## Architecture
Built adhering to clean architecture principles:
- **UI**: WPF (Windows Presentation Foundation) with custom modern styles, avoiding typical outdated WinForms looks.
- **MVVM**: Strict use of `CommunityToolkit.Mvvm` for ViewModels to maintain separation of concerns.
- **Data**: Microsoft.Data.Sqlite for fast, local persistence.
- **Services/Core**: Dependency Injection utilized for background trackers (`AppUsageTracker`), native API monitors (`ActiveWindowMonitor`), and core logic (`FocusManager`).

## Building & Running
See [BUILD.md](BUILD.md) for compilation instructions and prerequisites.
