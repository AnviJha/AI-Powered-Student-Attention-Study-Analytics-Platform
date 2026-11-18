"""Digital engagement heuristic adapted from FlowFocus attention_engine.py.

This is never a visual attention or mental-focus measurement. Weights are
provisional and should be evaluated against consented study data.
"""
def _clamp(value):
    return max(0.0, min(100.0, float(value)))


def score_digital(*, mouse_moves=0, mouse_clicks=0, keyboard_events=0,
                  tab_visible=True, idle_seconds=0):
    mouse = _clamp(mouse_moves * 0.4 + mouse_clicks * 8)
    keyboard = _clamp(keyboard_events * 6)
    visibility = 100.0 if tab_visible else 20.0
    inactivity = _clamp(100 - idle_seconds * 2.5)
    # Normalize only observed digital signals; never inject face/blink defaults.
    score = round(mouse * .28 + keyboard * .25 + visibility * .25 + inactivity * .22)
    return {"digital_engagement_score": int(_clamp(score)), "signal_breakdown": {
        "mouse_activity": round(mouse), "keyboard_activity": round(keyboard),
        "tab_visibility": round(visibility), "inactivity": round(inactivity)},
        "reasons": ["Digital interaction heuristic; not a visual attention estimate",
                    "Tab visible" if tab_visible else "Tab hidden",
                    f"Idle for {idle_seconds:g} seconds"]}

