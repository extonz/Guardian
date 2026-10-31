# Contributing

## Principles
- Keep the app local-first: no telemetry, cloud upload, window-title collection, keystroke logging, or screenshots.
- Never terminate another process as an app-blocking action. Blocking should remain reversible.
- Keep platform-independent logic in src/Guardian.Core so it can be unit-tested without WPF.
- Keep Windows API calls and WPF-specific code in src/Guardian.App.
- Add tests for changes to timing, usage aggregation, data normalization, and process rules.

## Development checks

Run from the repository root on Windows with the .NET 10 SDK:

\`\`\`powershell
dotnet restore Guardian.sln
dotnet build Guardian.sln -c Release
dotnet test tests/Guardian.Core.Tests/Guardian.Core.Tests.csproj -c Release
\`\`\`

Do not describe a build as verified unless the build and tests actually pass.
