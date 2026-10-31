using System.Text;
using System.Text.Json;
using Guardian.Core.Models;

namespace Guardian.Core.Storage;

public sealed class JsonStateStore
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    private readonly string _filePath;
    private readonly SemaphoreSlim _writeLock = new(1, 1);

    public JsonStateStore(string? filePath = null)
    {
        if (string.IsNullOrWhiteSpace(filePath))
        {
            var folder = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "Guardian");
            _filePath = Path.Combine(folder, "guardian-state.json");
        }
        else
        {
            _filePath = filePath;
        }
    }

    public string FilePath => _filePath;

    public async Task<(GuardianState State, string? Warning)> LoadAsync(CancellationToken cancellationToken = default)
    {
        if (!File.Exists(_filePath))
            return (new GuardianState(), null);

        try
        {
            var json = await File.ReadAllTextAsync(_filePath, cancellationToken);
            var state = JsonSerializer.Deserialize<GuardianState>(json, JsonOptions) ?? new GuardianState();
            state.Normalize();
            return (state, null);
        }
        catch (JsonException)
        {
            var backupPath = _filePath + ".corrupt-" + DateTimeOffset.Now.ToString("yyyyMMdd-HHmmss");
            try
            {
                File.Move(_filePath, backupPath, overwrite: false);
                return (new GuardianState(), $"The local data file was invalid. A backup was kept at {backupPath}.");
            }
            catch (IOException)
            {
                return (new GuardianState(), "The local data file could not be read. Guardian started with empty in-memory data; the original file was left untouched.");
            }
        }
        catch (Exception exception) when (exception is IOException or UnauthorizedAccessException)
        {
            return (new GuardianState(), $"Guardian could not read its local data file: {exception.Message}");
        }
    }

    public async Task SaveJsonAsync(string json, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(json);
        await _writeLock.WaitAsync(cancellationToken);

        var directory = Path.GetDirectoryName(_filePath);
        var temporaryPath = _filePath + ".tmp";

        try
        {
            if (!string.IsNullOrEmpty(directory))
                Directory.CreateDirectory(directory);

            await File.WriteAllTextAsync(temporaryPath, json, new UTF8Encoding(false), cancellationToken);
            File.Move(temporaryPath, _filePath, overwrite: true);
        }
        finally
        {
            try
            {
                if (File.Exists(temporaryPath))
                    File.Delete(temporaryPath);
            }
            catch (IOException)
            {
                // A failed cleanup must not hide the original persistence error.
            }

            _writeLock.Release();
        }
    }
}
