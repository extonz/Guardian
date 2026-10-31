using Guardian.Core.Storage;

namespace Guardian.Core.Tests;

public sealed class JsonStateStoreTests
{
    [Fact]
    public async Task LoadsVersion70StateWithoutDroppingExistingData()
    {
        var folder = Path.Combine(Path.GetTempPath(), "GuardianTests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(folder);
        var filePath = Path.Combine(folder, "guardian-state.json");

        try
        {
            await File.WriteAllTextAsync(filePath, """
                {
                  "Usage": [{ "Date": "2026-10-31", "Name": "chrome", "Seconds": 125.0 }],
                  "Sessions": [{ "Date": "2026-10-31T10:00:00", "Minutes": 25.0, "Completed": true }],
                  "Blocked": ["discord.exe"],
                  "TrackingEnabled": false,
                  "BlockingEnabled": true,
                  "ActiveFocusStarted": null,
                  "ActiveFocusMinutes": 0
                }
                """);

            var store = new JsonStateStore(filePath);
            var (state, warning) = await store.LoadAsync();

            Assert.Null(warning);
            Assert.Single(state.Usage);
            Assert.Equal(125, state.Usage[0].Seconds);
            Assert.Single(state.Sessions);
            Assert.Equal("discord", Assert.Single(state.Blocked));
            Assert.False(state.TrackingEnabled);
            Assert.True(state.BlockingEnabled);
        }
        finally
        {
            Directory.Delete(folder, recursive: true);
        }
    }

    [Fact]
    public async Task PreservesMalformedFileAsBackup()
    {
        var folder = Path.Combine(Path.GetTempPath(), "GuardianTests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(folder);
        var filePath = Path.Combine(folder, "guardian-state.json");

        try
        {
            await File.WriteAllTextAsync(filePath, "{ not valid json");
            var store = new JsonStateStore(filePath);

            var (state, warning) = await store.LoadAsync();

            Assert.Empty(state.Usage);
            Assert.NotNull(warning);
            Assert.False(File.Exists(filePath));
            Assert.Single(Directory.GetFiles(folder, "guardian-state.json.corrupt-*"));
        }
        finally
        {
            Directory.Delete(folder, recursive: true);
        }
    }
}
