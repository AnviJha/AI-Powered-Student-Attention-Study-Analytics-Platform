# Phase 02 — Backend and database foundation

## Objective and status

ACTIVE, partial. Establish authenticated study records and honest analytics that the existing UI can consume. Do not create visual scores, AI responses, or production XP from demo fixtures.

## Scope and features

FastAPI under `backend/app`, MongoDB collections (`users`, `sessions`, `attention_records`, `distractions`), JWT, profile preferences, session state transitions, derived digital score, period analytics, and an explainable focus plan. The current implementation is in `backend/app/main.py` and pure services under `backend/app/services/`.

## Execution order

1. Finish API contracts and split the current foundation into routers, schemas, and repositories when the behavior is stable; keep one scoring implementation.
2. Run indexes and authentication against a real test MongoDB; verify duplicate email handling and connection errors.
3. Add source, consent, and quality metadata before accepting future visual signals. Until then `visual_attention_score` stays `null`.
4. Extend analytics with timezone-aware calendar boundaries, focused time when validated visual records exist, baseline eligibility, and distraction categories. Return `null` where unavailable.
5. Add a frontend data adapter and login/register flow. Preserve explicit demo mode; wire session, profile, analytics, and focus-plan views to live APIs with loading, empty, and error states.
6. Add integration tests for each endpoint, race conditions, ownership, expired tokens, invalid input, and a real MongoDB instance.

## Dependencies and API

Install `backend/requirements-dev.txt` for tests and `backend/requirements.txt` for runtime. Set `MONGO_URI`, `MONGO_DB`, `JWT_SECRET` (32+ characters), and `CORS_ORIGINS`; never commit secrets. Current endpoints: `/api/health`, `/api/auth/register`, `/api/auth/login`, `/api/profile`, `/api/sessions`, `/api/sessions/{id}`, `/api/sessions/{id}/status/{pause|resume|end}`, `/api/sessions/{id}/digital-records`, `/api/sessions/{id}/attention-records`, `/api/sessions/{id}/distractions`, `/api/analytics?period=daily|weekly|monthly`, and `/api/focus/plan`. Except health and register/login, use Bearer JWT. IDs in dependent requests must identify a session owned by the token subject.

## Database and integration points

Users have a unique email index. Sessions and records index `user_id` and time/session keys. Durations are seconds, times are UTC, and returned times are ISO 8601. A live client must not submit `src/data.js` fixture values to these endpoints. No raw video field or upload endpoint exists.

## Testing, acceptance, and risks

Current isolated result: 5 tests passed with `mongomock`; this does not prove MongoDB connectivity. Exit requires a real MongoDB API run, frontend live/demo flow, authorization and validation tests, and accurate analytics with empty/missing-signal behavior. Risks: client-reported signals can be forged; heuristic weights are not validated; session time depends on server clock; browser storage for JWT needs a deliberate policy.

## Checklist

- [x] FastAPI, configuration, indexes, JWT, profile, sessions and owned record endpoints.
- [x] Digital engagement separated from visual attention; focus-plan fallback and reasons.
- [x] Isolated service and API tests.
- [ ] Real MongoDB test and connection/error handling.
- [ ] Frontend auth and live-data adapter.
- [ ] Analytics calendar/timezone and focused-time rules.
- [ ] Full failure-path and security review.

Depends on Phase 1 UI contracts. Phase 3 can begin only after consent and derived-signal contracts are documented.

