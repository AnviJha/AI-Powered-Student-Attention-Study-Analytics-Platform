from datetime import datetime, timezone
from bson import ObjectId

from app.services.engagement import score_digital
from app.services.planner import recommend_plan, break_check
from app.services.analytics import summarize


def test_digital_score_is_separate_and_bounded():
    quiet = score_digital(tab_visible=False, idle_seconds=1000)
    active = score_digital(mouse_moves=10000, keyboard_events=10000)
    assert 0 <= quiet["digital_engagement_score"] < active["digital_engagement_score"] <= 100
    assert "visual_attention_score" not in active
    assert active["reasons"]


def test_planner_default_trend_and_break():
    assert recommend_plan([])["confidence"] == "default"
    declining = recommend_plan([80, 80, 80, 50, 50, 50])
    assert declining["trend"] == "declining"
    assert declining["focus_minutes"] == 15
    assert break_check(13, 25, [20, 20, 20])["urgency"] == "early"
    assert break_check(25, 25, [80])["urgency"] == "scheduled"


def test_analytics_empty_and_missing_visual():
    now = datetime.now(timezone.utc)
    empty = summarize([], [], [], now=now)
    assert empty["data_status"] == "empty"
    assert empty["average_visual_attention_score"] is None
    session = {"_id": ObjectId(), "subject": "Math", "started_at": now, "active_seconds": 600}
    record = {"session_id": str(session["_id"]), "captured_at": now, "digital_engagement_score": 72}
    report = summarize([session], [record], [], now=now)
    assert report["session_count"] == 1
    assert report["study_seconds"] == 600
    assert report["average_digital_engagement_score"] == 72
    assert report["estimated_focused_seconds"] is None

