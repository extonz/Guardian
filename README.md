# Guardian 7.0

Guardian is a native Windows digital-wellbeing and focus app, rewritten in C# and WPF. Python is not required to run or build the new app.

## Features

- Foreground application time tracking, stored locally by application name.
- Focus timer with pause/resume and session history.
- Configurable app list that Guardian gently minimizes when a listed app becomes active.
- Separate controls for tracking and blocking.
- Local data deletion control.
- No telemetry, window-title collection, keystroke logging, screenshots, or network upload.

## Requirements

- Windows 10 or Windows 11
- .NET 10 SDK to build from source

## Build and run

From the repository root, run these commands in PowerShell:

    dotnet restore Guardian.csproj
    dotnet build Guardian.csproj -c Release
    dotnet run --project Guardian.csproj

To publish a self-contained 64-bit Windows executable:

    dotnet publish Guardian.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true

The output is in bin/Release/net10.0-windows/win-x64/publish/.

## Important limitations

Application detection uses the Windows foreground-window API and is best-effort. Blocking gently minimizes the foreground window and is intentionally reversible; it is not parental control or a security boundary. The application has not yet been verified by a Windows build in this development session, so build and runtime validation are still required.

The legacy Python implementation is being removed from this migration branch. The C# app is the intended application going forward.

## License

MIT. See LICENSE.