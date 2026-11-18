# Development roadmap

## Product and current state

The platform is a privacy-first study companion. It records study sessions and, in future phases, derived behavioral signals to explain *estimated* attention and study patterns. It cannot measure a student's mental state. The React presentation UI is owner-completed and builds successfully. Phase 2 is ACTIVE: a first backend foundation exists, but live frontend integration and a real MongoDB verification remain open.

## Phase sequence and dependency

| Phase | Status | Depends on | Major deliverable and exit gate |
| --- | --- | --- | --- |
| [1 UI](PHASE_01_UI.md) | Owner-completed; browser QA pending | None | Navigable demo, responsive UI, honest mock labels, successful build |
| [2 Backend](PHASE_02_BACKEND.md) | ACTIVE, partial | Phase 1 contracts | Authenticated owned sessions, records, analytics, API integration, test Mongo verification |
| [3 CV](PHASE_03_COMPUTER_VISION.md) | Upcoming | Phase 2 records and consent model | Opt-in local processing and validated derived visual signals |
| [4 Intelligence](PHASE_04_AI_PERSONALIZATION.md) | Upcoming | Sufficient valid Phase 2/3 data | Calibrated baseline, explainable plans, coach, gamification |
| [5 Integration](PHASE_05_INTEGRATION_DEPLOYMENT.md) | Upcoming | Phases 2–4 | End-to-end, security/privacy checks, deployment |

## Phase 2 progress and next tasks

Implemented: FastAPI app, MongoDB access and indexes, JWT accounts, profile and owned sessions, digital records, client-reported distraction records, period summaries, digital engagement heuristic, explainable focus planner, and isolated tests. No visual attention estimate or focused-time estimate is produced without real signals. Next: build the frontend live-data adapter and auth flow while preserving demo mode; then test against a real MongoDB instance.

## Cross-phase acceptance and testing

Each phase needs documented API/data contracts, validation, authorization where applicable, tests for business rules and failure paths, build/start commands, and evidence for real integrations. Mock output is never evidence that a camera, AI model, or reward engine works. See each phase document for its gate.

## Known risks

- FlowFocus thresholds are unvalidated heuristics; copy only with attribution and adaptation.
- Client-reported digital activity and distractions can be forged; do not treat them as verified attention.
- The current frontend is a monolithic React component with local fixtures; its data-access seam needs care to preserve the presentation flow.
- A real MongoDB server has not yet been used to verify the API; isolated tests use `mongomock`.
- The Phase 1 build warns about a large JavaScript bundle; optimize only after the live flow is stable.

