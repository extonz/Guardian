"""Optional, non-blocking native notifications."""
def notify(title: str, message: str) -> None:
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="Guardian", timeout=4)
    except Exception:
        # Notification services may be unavailable (e.g. minimal Linux desktops).
        return
