# Install Guardian 7

Guardian 7 is a native Windows desktop application written in C# and WPF. Python is not required.

Requirements: Windows 10/11 and the .NET 10 SDK.

From the repository root, run in PowerShell:

    dotnet restore Guardian.csproj
    dotnet build Guardian.csproj -c Release
    dotnet run --project Guardian.csproj

To publish a self-contained x64 executable:

    dotnet publish Guardian.csproj -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true

The output is in bin/Release/net10.0-windows/win-x64/publish/. Local state is stored under the user's LocalAppData/Guardian folder. The app does not upload activity data.