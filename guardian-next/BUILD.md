# Building Guardian Next

Guardian Next is a Windows Presentation Foundation (WPF) application targeting .NET 10.0.

## Prerequisites
- Windows OS (WPF only runs on Windows)
- .NET 10.0 SDK
- Visual Studio 2022 (recommended) or VS Code with C# Dev Kit

## Build via CLI
```bash
cd guardian-next
dotnet build Guardian.sln --configuration Release
```

## Running the app
```bash
dotnet run --project Guardian/Guardian.csproj
```

## Running Tests
```bash
dotnet test Guardian.sln
```

## Publishing a Standalone Executable
You can publish a self-contained executable that doesn't require users to install .NET 10:

```bash
dotnet publish Guardian/Guardian.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o out
```

The executable will be located in the `out` directory.

## Note on Linux/macOS
Because WPF relies on Windows UI components, you cannot run or test this application on Linux or macOS. The source code can be edited using any text editor, but compilation and execution must be performed on Windows (or via a Windows CI runner, like the configured GitHub Actions workflow).
