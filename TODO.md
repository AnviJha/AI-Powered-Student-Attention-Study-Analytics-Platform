# Project TODO

## Phase 1 — Complete UI Development and Presentation

**Status: owner-completed; production build verified. Browser and responsive visual QA remain open.** See [Phase 1](docs/development/PHASE_01_UI.md).

- [x] Inspect the existing repository and identify the current frontend setup before editing (documentation-only repository).
- [x] Complete the full student-facing UI described in `docs/UI_REQUIREMENTS.md`.
- [x] Implement the global app shell, navigation, responsive layout, and reusable components.
- [x] Implement all planned screens: Dashboard, Study Session, Analytics, AI Study Coach, Goals & Challenges, Achievements, and Profile/Settings.
- [x] Use realistic, consistent mock data for attention scores, focus time, distraction events, charts, AI insights, XP, levels, streaks, and badges.
- [x] Make primary navigation and key UI controls interactive using frontend state.
- [x] Implement useful empty and camera-permission preview states; local fixture views load immediately.
- [x] Add desktop, tablet, and mobile responsive layouts.
- [x] Verify the production build succeeds with Vite.
- [x] Prepare a presentation/demo flow that requires no backend or webcam.
- [x] Clearly distinguish simulated data and simulated AI/CV features from real functionality.
- [ ] Record browser interaction, console, keyboard, and responsive visual QA at mobile/tablet/desktop widths.

**Phase 1 exit criteria:** The complete UI is navigable, visually consistent, responsive, uses coherent demo data, has no dead primary navigation, and can be demonstrated without a backend or webcam-processing service.

## Phase 2 — Backend and Data Layer (ACTIVE)

See [Phase 2 implementation guide](docs/development/PHASE_02_BACKEND.md) and [FlowFocus integration](docs/FLOWFOCUS_INTEGRATION.md).

- [x] Establish FastAPI app, dependency files, environment example, and health endpoint.
- [x] Add MongoDB client, project collections, and user/session/record indexes (isolated test only).
- [x] Add validated registration, login, JWT authorization, and profile APIs.
- [x] Add owned study-session start/list/detail/pause/resume/end APIs.
- [x] Add owned digital-record and client-reported distraction-record APIs; keep visual score unavailable.
- [x] Add provisional digital engagement and explainable focus-planning services adapted from FlowFocus.
- [x] Add daily/weekly/monthly analytics foundation with missing-signal states.
- [x] Add a separate recorded-data frontend workspace for auth, sessions, analytics, and focus plans; preserve demo screens.
- [x] Add isolated API/service tests (5 passing with mongomock).
- [ ] Verify database startup, indexes, duplicate-email behavior, and API flows against a real MongoDB instance.
- [ ] Browser-test the recorded workspace and API errors at desktop/tablet/mobile widths.
- [ ] Complete a shared frontend data adapter so existing Dashboard, Session, Analytics, and Profile screens can use recorded data when selected.
- [ ] Define calendar/timezone aggregation and validated visual-signal/focused-time contracts before accepting visual records.
- [ ] Expand authorization, validation, concurrency, expired-token, and failure-path tests.
- [ ] Review authentication token handling and production configuration before deployment.

## Phase 3 — Computer Vision and Attention Estimation (UPCOMING; see [guide](docs/development/PHASE_03_COMPUTER_VISION.md))

- [ ] Prototype local webcam permission and capture flow.
- [ ] Implement face-presence detection.
- [ ] Implement head-pose estimation with MediaPipe/OpenCV.
- [ ] Evaluate feasible eye/gaze-direction signals and document limitations.
- [ ] Define distraction-event rules and thresholds.
- [ ] Implement an explainable attention-estimation engine.
- [ ] Evaluate optional YOLO-based phone detection.
- [ ] Ensure raw webcam footage is not stored by default.
- [ ] Integrate derived signals with the backend.

## Phase 4 — Personalization, ML, GenAI, and Gamification Logic (UPCOMING; see [guide](docs/development/PHASE_04_AI_PERSONALIZATION.md))

- [ ] Define reliable attention and focus metrics.
- [ ] Calculate personal attention baselines from sufficient history.
- [ ] Detect time-of-day and session-duration patterns.
- [ ] Evaluate predictive models only when enough quality data exists.
- [ ] Integrate one GenAI provider for structured-data-based coaching.
- [ ] Implement grounded, explainable recommendations.
- [ ] Implement XP, levels, badges, streaks, goals, and challenge rules.
- [ ] Add anti-gaming rules so timer duration alone does not earn focus rewards.

## Phase 5 — Integration, Testing, Privacy, and Deployment (UPCOMING; see [guide](docs/development/PHASE_05_INTEGRATION_DEPLOYMENT.md))

- [ ] Integrate frontend, backend, CV, and intelligence services.
- [ ] Add automated tests and end-to-end tests.
- [ ] Perform security and privacy review.
- [ ] Add Docker configuration and deployment pipeline.
- [ ] Deploy frontend, backend, and database.
- [ ] Validate monitoring, error handling, and production configuration.

## Scope rule

Phase 2 was authorized after the presentation UI. Keep Phase 3–5 implementation pending until their prerequisites are met. Demo values must never be stored or described as measured records.
