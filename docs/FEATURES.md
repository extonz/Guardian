# Guardian 7 features

- Native C# / WPF Windows desktop interface.
- Foreground application time tracking, stored locally by application name.
- Focus timer with pause, resume, stop, and local session history.
- Configurable app list that Guardian can gently minimize when active.
- Separate persisted controls for tracking and blocking.
- Local data deletion control.
- No telemetry, window-title collection, keystroke logging, screenshots, or network upload.

## Limitations

Foreground-window detection is best-effort. App blocking is a productivity aid, not a security boundary: the user can reopen an application. Windows-critical processes are excluded from the block list. A Windows build and runtime verification are still required.