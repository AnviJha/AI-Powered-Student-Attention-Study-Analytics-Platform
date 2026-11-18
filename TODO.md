# Project TODO

## Phase 1 — Complete UI Development and Presentation

**Priority: ACTIVE — this is the only phase to work on now.**

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

**Phase 1 exit criteria:** The complete UI is navigable, visually consistent, responsive, uses coherent demo data, has no dead primary navigation, and can be demonstrated without a backend or webcam-processing service.

## Phase 2 — Backend and Data Layer (NOT ACTIVE)

- [ ] Design and implement FastAPI application structure.
- [ ] Configure MongoDB/MongoDB Atlas.
- [ ] Implement authentication and JWT flows.
- [ ] Implement user/profile and study-session APIs.
- [ ] Implement attention-event and distraction-event ingestion APIs.
- [ ] Implement analytics aggregation APIs.
- [ ] Connect frontend to real APIs and replace mock data incrementally.
- [ ] Add validation, authorization, tests, and API documentation.

## Phase 3 — Computer Vision and Attention Estimation (NOT ACTIVE)

- [ ] Prototype local webcam permission and capture flow.
- [ ] Implement face-presence detection.
- [ ] Implement head-pose estimation with MediaPipe/OpenCV.
- [ ] Evaluate feasible eye/gaze-direction signals and document limitations.
- [ ] Define distraction-event rules and thresholds.
- [ ] Implement an explainable attention-estimation engine.
- [ ] Evaluate optional YOLO-based phone detection.
- [ ] Ensure raw webcam footage is not stored by default.
- [ ] Integrate derived signals with the backend.

## Phase 4 — Personalization, ML, GenAI, and Gamification Logic (NOT ACTIVE)

- [ ] Define reliable attention and focus metrics.
- [ ] Calculate personal attention baselines from sufficient history.
- [ ] Detect time-of-day and session-duration patterns.
- [ ] Evaluate predictive models only when enough quality data exists.
- [ ] Integrate one GenAI provider for structured-data-based coaching.
- [ ] Implement grounded, explainable recommendations.
- [ ] Implement XP, levels, badges, streaks, goals, and challenge rules.
- [ ] Add anti-gaming rules so timer duration alone does not earn focus rewards.

## Phase 5 — Integration, Testing, Privacy, and Deployment (NOT ACTIVE)

- [ ] Integrate frontend, backend, CV, and intelligence services.
- [ ] Add automated tests and end-to-end tests.
- [ ] Perform security and privacy review.
- [ ] Add Docker configuration and deployment pipeline.
- [ ] Deploy frontend, backend, and database.
- [ ] Validate monitoring, error handling, and production configuration.

## Scope rule

Do not start Phase 2–5 work during the presentation UI phase unless the project owner explicitly changes the priority. Do not build real webcam processing, database persistence, authentication services, prediction models, or LLM API calls just to make the UI appear functional. Use mock data and clearly simulated interactions for the presentation.
