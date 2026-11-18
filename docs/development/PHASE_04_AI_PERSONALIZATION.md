# Phase 04 — Intelligence, personalization, GenAI, and gamification

## Objective and status

Upcoming. Build grounded personal guidance from sufficient valid history. Depends on Phase 2 records and Phase 3 visual-signal quality where visual conclusions are used.

## Scope, features, and order

1. Define eligibility and quality gates for personal visual baseline and time-of-day patterns; show insufficient-data states.
2. Calibrate the Phase 2 focus planner against recorded history and study outcomes; retain reasons, trend, sample count, and provisional heuristic status.
3. Adapt FlowFocus's rule-based recommendation structure to shorter sessions, manageable targets, breaks, and practice. Exclude quiz-course actions unless that product area is explicitly added.
4. Add one GenAI Study Coach provider behind a service boundary. Send structured, minimal analytics; validate response shape, cite input metrics in explanations, and use a deterministic fallback on provider failure. No raw webcam frames.
5. Define XP, levels, badges, streaks, daily challenges, and records with server-side anti-gaming rules. Reward verified meaningful progress rather than elapsed timer alone.
6. Consider prediction only after a dataset, target, baseline model, and evaluation plan exist.

## Files, dependencies, APIs, database

Expected modules: baseline, planner calibration, recommendation rules, coach adapter, reward rules, and tests. Add a provider SDK only when a provider is selected. Extend owned analytics storage for baseline and reward events with rule version and timestamps. APIs should return reasons, data eligibility, and provenance for each recommendation or reward. The React Coach, Goals, and Achievements screens consume these APIs after the backend rules pass tests.

## Tests and acceptance

Test low sample counts, declining trends, conflicting recommendations, provider timeout/malformed output, fabricated client claims, duplicate rewards, and cross-user isolation. Acceptance requires grounded explanations, no unsupported psychological conclusions, server-owned reward calculations, and correct fallback behavior.

## Risks and checklist

Historical bias, noisy visual signals, cost, prompt leakage, and reward gaming are key risks.

- [ ] Baseline eligibility and calibration.
- [ ] Study-specific recommendation rules.
- [ ] Structured-data AI Coach with fallback.
- [ ] Server-side gamification with anti-gaming tests.
- [ ] Prediction evaluation if sufficient data exists.

