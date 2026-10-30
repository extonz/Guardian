"""Small helpers for dashboard summaries."""
from datetime import date
from .storage import load

def summary() -> dict:
    stats = load("stats")
    events = stats.get("events", [])
    today = date.today().isoformat()
    today_events = [event for event in events if isinstance(event, dict) and str(event.get("at", "")).startswith(today)]
    return {"blocks": int(stats.get("blocks", 0)), "focus_minutes": int(stats.get("focus_minutes", 0)), "sessions": int(stats.get("sessions", 0)), "today_events": len(today_events)}
