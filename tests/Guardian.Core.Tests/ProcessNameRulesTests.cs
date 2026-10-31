using Guardian.Core.Services;

namespace Guardian.Core.Tests;

public sealed class ProcessNameRulesTests
{
    [Theory]
    [InlineData("Discord", "Discord")]
    [InlineData(" chrome.exe ", "chrome")]
    [InlineData("game_client-2.exe", "game_client-2")]
    public void NormalizesProcessNames(string input, string expected)
    {
        Assert.True(ProcessNameRules.TryNormalize(input, out var normalized));
        Assert.Equal(expected, normalized);
    }

    [Theory]
    [InlineData("")]
    [InlineData("C:\\Program Files\\Chrome\\chrome.exe")]
    [InlineData("https://example.com")]
    [InlineData("../explorer")]
    public void RejectsPathsAndNonProcessValues(string input)
    {
        Assert.False(ProcessNameRules.TryNormalize(input, out _));
    }

    [Theory]
    [InlineData("explorer")]
    [InlineData("taskmgr.exe")]
    [InlineData("winlogon")]
    public void ProtectsRecoveryAndWindowsCriticalProcesses(string input)
    {
        Assert.True(ProcessNameRules.TryNormalize(input, out var normalized));
        Assert.True(ProcessNameRules.IsProtected(normalized));
    }
}
