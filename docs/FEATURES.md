# Guardian 7.1 features

## Activity overview
- Samples the foreground process name approximately once per second.
- Aggregates active time by app and local calendar day.
- Attributes each observed interval to the app that was active at the previous observation.
- Discards gaps longer than five seconds instead of counting sleep or a stalled process as usage.
- Does not store window titles or document/browser content.

## Focus sessions
- 15, 25, 45, and 60-minute presets in the interface.
- Pause, resume, early stop, and completion history.
- Monotonic countdown timing, independent of wall-clock changes.
- A running session is recorded as interrupted when Guardian exits.

## App rules
- App names are matched against the Windows process name, not a URL or display name.
- Matching foreground windows are minimized; other processes are never terminated.
- Critical Windows processes, Guardian itself, and Task Manager are excluded.
- Rules can be disabled globally or removed individually.

## Privacy and storage
- Local JSON storage in %LOCALAPPDATA%\Guardian\guardian-state.json.
- Atomic temporary-file replacement to reduce the risk of a partially-written state file.
- Existing 7.0 JSON data is retained by the 7.1 state model.
- No telemetry or network data transfer.

## Limitations
- Usage totals are estimates based on polling, not OS-level forensic measurements.
- Minimizing a window is reversible and not tamper-proof.
- The WPF app must be built and run on Windows for full validation.
