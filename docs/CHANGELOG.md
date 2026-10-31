# Changelog

## 7.1.0
- Split platform-independent focus, usage, and process-rule logic into a dedicated .NET library.
- Added unit tests for app-switch accounting, midnight boundaries, sleep gaps, timer pause/resume, state migration, and protected process names.
- Attribute elapsed time to the previously observed foreground process instead of the newly observed one.
- Discard usage intervals after long polling gaps.
- Replaced per-second synchronous disk writes with periodic asynchronous writes and atomic file replacement.
- Preserved the 7.0 local JSON data shape and added malformed-file backup handling.
- Use a monotonic focus countdown and record sessions interrupted by app shutdown.
- Keep app blocking reversible and minimize windows instead of closing or terminating processes.
- Replaced stale Python and prototype build workflows with .NET 10 Windows build/test/release workflows.

## 7.0.0
- Initial native C# / WPF rewrite.
