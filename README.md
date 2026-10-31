# Guardian 7.1

Guardian is a native Windows digital-wellbeing app built with C# and WPF. It helps you understand foreground app use, run focus sessions, and apply reversible app-minimizing rules.

## What it does

- Tracks the process name of the foreground app and estimates active time.
- Splits usage at local midnight and discards long sampling gaps (such as when the PC sleeps).
- Offers focus sessions with pause, resume, and a recorded session history.
- Minimizes configured apps while they are foregrounded. It never terminates another process.
- Keeps settings, app rules, usage totals, and focus history on the local PC.
- Does not collect window titles, keystrokes, screenshots, browser contents, or send telemetry.

## Project structure

- src/Guardian.Core: platform-independent models and tested usage/focus logic.
- src/Guardian.App: Windows-only WPF interface and Windows foreground-window integration.
- tests/Guardian.Core.Tests: unit tests for the logic that can be tested without WPF.

## Requirements

- Windows 10 or Windows 11.
- .NET 10 SDK to build from source. End users can run a self-contained published build without installing the .NET runtime separately.

## Build and run

From the repository root in PowerShell:

\`\`\`powershell
dotnet restore Guardian.sln
dotnet build Guardian.sln -c Release
dotnet test tests/Guardian.Core.Tests/Guardian.Core.Tests.csproj -c Release
dotnet run --project src/Guardian.App/Guardian.App.csproj
\`\`\`

To publish a self-contained 64-bit Windows executable:

\`\`\`powershell
dotnet publish src/Guardian.App/Guardian.App.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o artifacts/Guardian
\`\`\`

The executable is written to artifacts/Guardian/Guardian.exe.

## Local data and migration

Guardian stores its state in:

    %LOCALAPPDATA%\Guardian\guardian-state.json

Version 7.1 keeps the existing JSON field names used by 7.0, so usage totals, completed sessions, block rules, and preferences are retained when the app is upgraded. If the file is malformed, Guardian attempts to preserve it as a timestamped .corrupt-* backup rather than silently overwriting it.

## Accuracy and limitations

Foreground usage is sampled approximately once per second. Time between observations is attributed to the app seen at the earlier observation, so an app switch can be off by up to roughly one polling interval. Gaps longer than five seconds are discarded to avoid counting sleep or long pauses.

App blocking is intentionally a soft block: Guardian minimizes the foreground window of a listed process. Users can still reopen the app, and this is not a security boundary, parental-control system, or tamper-proof restriction. Windows-critical processes and Task Manager are protected from being added to the block list.

Guardian is Windows-only because its desktop interface and foreground-window integration use WPF and the Windows API.

## Validation

The core logic has automated unit tests. A successful Windows build and an interactive runtime test are still required before treating any release artifact as verified. The GitHub Actions workflows build and test the solution on Windows when Actions are enabled for the repository.

## License

MIT. See LICENSE.
