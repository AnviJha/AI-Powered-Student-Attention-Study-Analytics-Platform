"""Study planner adapted from FlowFocus focus_planner.py (group-project code).

Uses only recorded, non-demo score history. Thresholds are unvalidated.
"""
import math


def _clean(values):
    return [max(0., min(100., float(x))) for x in (values or [])
            if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)]


def recommend_plan(scores):
    window = _clean(scores)[-30:]
    n = len(window)
    result = {"focus_minutes": 25, "break_minutes": 5, "long_break_minutes": 15,
              "cycles_before_long_break": 4, "average_score": None,
              "trend": "unknown", "sample_count": n,
              "confidence": "default" if n < 3 else "low" if n < 10 else "medium" if n < 30 else "high",
              "reasons": [], "heuristic": True}
    if n < 3:
        result["reasons"].append("Not enough recorded history; this is a starting 25/5 suggestion.")
        return result
    average = sum(window) / n
    result["average_score"] = round(average, 1)
    for upper, focus, rest in [(40, 10, 3), (55, 15, 5), (70, 20, 5), (85, 25, 5), (101, 30, 5)]:
        if average < upper:
            break
    result["focus_minutes"], result["break_minutes"] = focus, rest
    result["reasons"].append(f"Recent recorded score average is {average:.1f}; a {focus}-minute block is suggested.")
    if n >= 6:
        third = n // 3
        delta = sum(window[-third:]) / third - sum(window[:third]) / third
        result["trend"] = "declining" if delta <= -10 else "improving" if delta >= 10 else "steady"
        if result["trend"] == "declining":
            result["focus_minutes"] = max(10, focus - 5)
            result["reasons"].append("Recent scores declined; the block was shortened by five minutes.")
        elif result["trend"] == "improving":
            result["focus_minutes"] = min(35, focus + 5)
            result["reasons"].append("Recent scores improved; the block was extended by five minutes.")
    return result


def break_check(elapsed_minutes, focus_minutes, recent_scores):
    elapsed = max(0., float(elapsed_minutes))
    scores = _clean(recent_scores)
    if elapsed >= focus_minutes:
        return {"take_break": True, "urgency": "scheduled", "reason": "The suggested study block has ended."}
    if elapsed >= focus_minutes / 2 and len(scores) >= 3 and sum(scores[-3:]) / 3 < 35:
        return {"take_break": True, "urgency": "early", "reason": "Recent scores declined; consider an early break."}
    return {"take_break": False, "urgency": "none", "minutes_left": round(focus_minutes - elapsed, 1),
            "reason": "No break suggested yet."}

