namespace Guardian.Core.Services;

public static class ProcessNameRules
{
    private static readonly HashSet<string> Protected = new(StringComparer.OrdinalIgnoreCase)
    {
        "guardian", "explorer", "dwm", "csrss", "winlogon", "wininit", "services",
        "lsass", "smss", "svchost", "taskmgr", "sihost", "system", "registry",
        "applicationframehost", "shellexperiencehost", "startmenuexperiencehost"
    };

    public static bool TryNormalize(string? value, out string normalized)
    {
        normalized = "";
        var candidate = (value ?? "").Trim();

        if (candidate.EndsWith(".exe", StringComparison.OrdinalIgnoreCase))
            candidate = candidate[..^4];

        if (candidate.Length is 0 or > 128)
            return false;

        if (candidate.Any(character =>
                !char.IsLetterOrDigit(character) &&
                character is not '.' and not '_' and not '-'))
            return false;

        if (candidate is "." or "..")
            return false;

        normalized = candidate;
        return true;
    }

    public static bool IsProtected(string? processName) =>
        !string.IsNullOrWhiteSpace(processName) && Protected.Contains(processName);
}
