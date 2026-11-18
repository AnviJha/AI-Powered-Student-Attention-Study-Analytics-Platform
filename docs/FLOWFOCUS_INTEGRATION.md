# FlowFocus integration assessment

## Repository and permission

`dummy/` was a separate FlowFocus checkout with `app/api`, `app/core`, `app/models`, `app/services`, and `tests`. The main project initially had a Vite React UI, `src/data.js` fixtures, and no backend. FlowFocus had no tracked LICENSE file or README license grant. On 2026-11-18 the project owner stated the code belongs to a group-project collaborator and expressly authorized its use for this project. This is the basis for the selected adaptations. After assessment, the owner requested deletion of `/dummy`; it has been removed and is not a runtime dependency. Attribution is recorded in adapted module docstrings and this document. If the group later adds a formal license or notice, preserve its conditions.

## File-by-file mapping

| FlowFocus file | Main-project location | Decision and change |
| --- | --- | --- |
| `app/services/focus_planner.py` | `backend/app/services/planner.py` | Adapted tier/trend, sample-confidence, early/long-break logic; renamed score source and explanations for study history. Thresholds remain provisional. |
| `tests/test_focus_planner.py` | `backend/tests/test_services.py` | Adapted key default, trend, and break cases; broader boundary coverage remains. |
| `app/services/attention_engine.py` | `backend/app/services/engagement.py` | Adapted digital activity weighting only. Removed face/blink and course/quiz signals; output is `digital_engagement_score`, never visual attention. |
| `tests/test_attention_engine.py` | `backend/tests/test_services.py` | Adapted boundedness and missing-visual distinction; full signal boundary suite remains. |
| `app/services/adaptive_engine.py` | Phase 4 recommendation service | Rule/reasons design evaluated; no quiz-specific code imported in Phase 2. |
| `tests/test_adaptive_engine.py` | Phase 4 tests | Test pattern evaluated; no test imported yet. |
| `app/api/reports.py` | `backend/app/services/analytics.py`, `/api/analytics` | Independently adapted aggregation concept. Uses owned study sessions and derived records; no course/quiz data and no write on read. |
| `app/api/auth/auth.py` | `backend/app/main.py` auth routes | Adapted bcrypt and JWT approach; tighter validation and user lookup on every token use. Guest auth omitted. |
| `app/api/auth/session.py` | None | Empty duplicate-session placeholder; excluded. |
| `app/api/session.py` | `backend/app/main.py` session routes | Adapted owner-scoped lifecycle for subject/topic sessions, including pause/resume and server-tracked active time. |
| `app/models/user.py` | `backend/app/main.py` request schemas | Adapted email/password/profile shapes with constraints. |
| `app/models/session.py` | `backend/app/main.py` request and response contracts | Replaced course/lesson fields with study subject, topic, goal, and status. |
| `app/core/security.py` | `backend/app/main.py` auth dependency | Adapted bearer JWT pattern; token subject is resolved to an existing user. |
| `app/core/database.py`, `app/core/config.py` | `backend/app/main.py`, `backend/.env.example` | Adapted MongoDB/env approach with lazy client and project-specific DB/indexes; no import-time connection. |
| `app/api/attention.py`, `app/models/attention.py` | `/api/sessions/{id}/digital-records` and `/attention-records` | Derived digital records only for Phase 2. Visual fields remain `null`; raw frames are excluded. |
| `app/api/activity.py`, `app/models/activity.py` | `backend/app/services/engagement.py`, digital-record API | Adapted aggregate signal idea; no raw mouse coordinates or WebSocket fanout. |
| `app/api/focus.py`, `app/models/focus.py` | `/api/focus/plan` | Adapted owned historical-plan endpoint; focus mini-game storage excluded. |
| `app/services/gemini_client.py` | Phase 4 AI Coach adapter | Pattern reviewed; no provider dependency or call added. |
| `app/services/ai_course_generator.py` | None | Excluded course/lesson/quiz generation; not the Study Coach. |
| `app/services/quiz_grader.py` | None | Excluded quiz system. |
| `app/api/ws.py`, `app/core/ws_manager.py` | None | Deferred. FlowFocus WebSocket route lacks authentication and its hub is in-memory. |
| `app/main.py` | `backend/app/main.py` | Adapted FastAPI/CORS/router concept; no wholesale application import. |

FlowFocus's course, lesson, progress, practice, and quiz models/routes are intentionally excluded. It has no completed gamification engine; this project will build that separately in Phase 4.

## Architectural differences and data contracts

FlowFocus mixes mouse, keyboard, tab, inactivity, optional face/blink, lesson, and quiz signals into one `interaction_score` and also exposes it as `attention_score`. This project maintains three separate concepts: `digital_engagement_score` (Phase 2 heuristic), `visual_attention_score` (unavailable until Phase 3), and `combined_study_engagement` (unavailable until a calibrated combination exists). `null` means unavailable, not zero. The Phase 2 focus plan uses digital scores and labels its `score_source`; later visual-history planning must be reviewed independently.

All new records include a user ID and an owned session ID. Times are UTC, durations seconds. The API stores no raw webcam video. Digital activity and distraction events are client reported and can be forged, so they are not validated attention or rewards. A live frontend view is isolated under **Recorded workspace**; original screens still use mock data and keep their demo labels.

## Dependencies, tests, and outstanding work

Backend runtime dependencies: FastAPI, Uvicorn, PyMongo, python-jose with cryptography, bcrypt, email-validator. Test dependencies: pytest, httpx, mongomock. No Gemini, OpenCV, MediaPipe, YOLO, or ML dependency was added. Existing React dependencies remain unchanged.

`python -m pytest -q` in `backend/`: 5 passed using `mongomock`. `npm run build`: passed, with a bundle-size warning. These results do not prove a real MongoDB connection, browser interactions, or responsive visual quality. Next work: real MongoDB verification, frontend live-mode browser QA, stronger API boundary tests, timezone-aware calendar analytics, and focused-time rules after valid visual signals exist. See [Phase 2](development/PHASE_02_BACKEND.md).
