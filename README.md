# Guardian v6.0

Guardian is a cross-platform digital-wellbeing desktop app. This version is isolated under `guardian-v6/` so the existing v5 files and user data remain untouched while v6 is reviewed.

## Install

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Linux requires a working Tk installation. On Debian/Ubuntu: `sudo apt install python3-tk`.

## Notes

- App detection is best-effort and platform-dependent. Linux Wayland may restrict active-window detection; macOS may require Accessibility permission.
- Guardian does not terminate applications. It detects configured app titles and offers non-blocking reminders.
- Data lives in the platform's user-data directory, not the current working directory.
- Run tests with `python -m pytest`.

## Build

GitHub Actions builds Windows, macOS and Linux packages on a tag (`v6.0.0`, etc.) or manual dispatch. Artifacts are uploaded per OS; release creation runs once after all builds finish.
