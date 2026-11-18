"""Pure aggregation of owned study records. Missing scores remain missing."""
from collections import defaultdict
from datetime import datetime, timedelta, timezone


def summarize(sessions, records, distractions, period="daily", now=None):
    now = now or datetime.now(timezone.utc)
    start = (now - timedelta(days={"daily": 1, "weekly": 7, "monthly": 30}[period]))
    selected = [s for s in sessions if s.get("started_at") and s["started_at"] >= start]
    ids = {str(s["_id"]) for s in selected}
    valid = [r for r in records if r.get("session_id") in ids and r.get("captured_at") and r["captured_at"] >= start]
    events = [d for d in distractions if d.get("session_id") in ids and d.get("occurred_at") and d["occurred_at"] >= start]
    duration = sum(s.get("active_seconds", 0) for s in selected)
    focused = sum(s.get("focused_seconds", 0) for s in selected)
    visual = [r["visual_attention_score"] for r in valid if r.get("visual_attention_score") is not None]
    digital = [r["digital_engagement_score"] for r in valid if r.get("digital_engagement_score") is not None]
    by_day = defaultdict(lambda: {"study_seconds": 0, "focused_seconds": 0, "sessions": 0})
    for session in selected:
        day = session["started_at"].date().isoformat()
        by_day[day]["study_seconds"] += session.get("active_seconds", 0)
        by_day[day]["focused_seconds"] += session.get("focused_seconds", 0)
        by_day[day]["sessions"] += 1
    return {"period": period, "session_count": len(selected), "study_seconds": duration,
            "estimated_focused_seconds": focused if visual else None,
            "average_visual_attention_score": round(sum(visual)/len(visual), 1) if visual else None,
            "average_digital_engagement_score": round(sum(digital)/len(digital), 1) if digital else None,
            "combined_study_engagement": None, "potential_distraction_count": len(events),
            "longest_session_seconds": max((s.get("active_seconds", 0) for s in selected), default=0),
            "by_day": [{"date": day, **values} for day, values in sorted(by_day.items())],
            "recent_sessions": [{"id": str(s["_id"]), "subject": s["subject"], "topic": s.get("topic"),
                                 "started_at": s["started_at"].isoformat(), "active_seconds": s.get("active_seconds", 0)}
                                for s in sorted(selected, key=lambda s:s["started_at"], reverse=True)[:10]],
            "data_status": "recorded" if selected else "empty"}
