# Installation and development

## Run from source

Requirements:
- Windows 10 or Windows 11
- .NET 10 SDK

From the repository root:

\`\`\`powershell
dotnet restore Guardian.sln
dotnet build Guardian.sln -c Release
dotnet test tests/Guardian.Core.Tests/Guardian.Core.Tests.csproj -c Release
dotnet run --project src/Guardian.App/Guardian.App.csproj
\`\`\`

## Publish a standalone executable

\`\`\`powershell
dotnet publish src/Guardian.App/Guardian.App.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o artifacts/Guardian
\`\`\`

The application is written to artifacts/Guardian/Guardian.exe.

## Existing 7.0 data

The 7.1 app continues using %LOCALAPPDATA%\Guardian\guardian-state.json and keeps the existing JSON property names. Back up that file before manually editing it. If Guardian cannot parse it, it attempts to move the malformed file to a timestamped backup rather than replacing it.

## Notes

Guardian uses Windows Presentation Foundation (WPF) and the Windows foreground-window API. The desktop application is not supported on Linux or macOS.
