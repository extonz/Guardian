# Contributing to Guardian

- The active application is C# / .NET 10 with WPF and targets Windows.
- Keep foreground monitoring lightweight and avoid collecting window titles or sensitive user content.
- Store activity locally and never add telemetry or remote upload without an explicit product/privacy review.
- Keep app blocking reversible and do not terminate processes or target Windows-critical applications.
- Build with `dotnet build Guardian.csproj -c Release` on Windows with the .NET 10 SDK.
- Do not claim the project builds or tests pass unless the commands have actually been run.
