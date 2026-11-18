"""Calendar-period aggregation of owned study records.

Missing visual evidence remains None. Sessions are assigned to the period in
which they started; splitting a session across midnight is future work.
"""
from collections import Counter, defaultdict
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo


def summarize(sessions, records, distractions, period="daily", now=None, time_zone="UTC"):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone aware")
    zone = ZoneInfo(time_zone)
    local_now = now.astimezone(zone)
    local_date = local_now.date()
    if period == "daily":
        start_date = local_date
    elif period == "weekly":
        start_date = local_date.fromordinal(local_date.toordinal() - local_date.weekday())
    elif period == "monthly":
        start_date = local_date.replace(day=1)
    else:
        raise ValueError("Unsupported period")
    start = datetime.combine(start_date, time.min, zone).astimezone(timezone.utc)
    current = now.astimezone(timezone.utc)

    selected = [s for s in sessions if s.get("started_at") and start <= s["started_at"] <= current]
    ids = {str(s["_id"]) for s in selected}
    valid = [r for r in records if r.get("session_id") in ids and r.get("captured_at") and start <= r["captured_at"] <= current]
    events = [d for d in distractions if d.get("session_id") in ids and d.get("occurred_at") and start <= d["occurred_at"] <= current]
    digital = [r["digital_engagement_score"] for r in valid if r.get("digital_engagement_score") is not None]
    # Visual ingestion is intentionally unavailable in Phase 2. Merely finding a
    # score in a stored record cannot establish validated visual attention.
    total_seconds = sum(s.get("active_seconds", 0) for s in selected)
    by_day = defaultdict(lambda: {"study_seconds": 0, "estimated_focused_seconds": None, "sessions": 0})
    for session in selected:
        day = session["started_at"].astimezone(zone).date().isoformat()
        by_day[day]["study_seconds"] += session.get("active_seconds", 0)
        by_day[day]["sessions"] += 1
    categories = Counter(d.get("category", "other") for d in events)
    return {
        "period": period, "time_zone": time_zone, "period_start": start.isoformat(), "period_end": current.isoformat(),
        "session_count": len(selected), "study_seconds": total_seconds,
        "estimated_focused_seconds": None, "average_visual_attention_score": None,
        "average_digital_engagement_score": round(sum(digital) / len(digital), 1) if digital else None,
        "combined_study_engagement": None, "potential_distraction_count": len(events),
        "distraction_categories": dict(categories),
        "focus_efficiency": None, "personal_visual_baseline": None, "best_study_window": None,
        "longest_session_seconds": max((s.get("active_seconds", 0) for s in selected), default=0),
        "by_day": [{"date": day, **values} for day, values in sorted(by_day.items())],
        "recent_sessions": [{"id": str(s["_id"]), "subject": s["subject"], "topic": s.get("topic"),
                             "started_at": s["started_at"].isoformat(), "active_seconds": s.get("active_seconds", 0)}
                            for s in sorted(selected, key=lambda s: s["started_at"], reverse=True)[:10]],
        "data_status": "recorded" if selected else "empty",
    }
