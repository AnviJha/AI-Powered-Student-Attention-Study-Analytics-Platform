# Development roadmap

## Product and current state

The platform is a privacy-first study companion. It records study sessions and optional derived behavioral signals. It cannot measure a student's mental state. The React presentation UI is owner-completed and builds successfully. Phase 3 is ACTIVE: a browser-local visual-signal prototype and owned API are implemented; real-camera evaluation remains open. Phase 2 browser acceptance checks also remain open.

## Phase sequence and dependency

| Phase | Status | Depends on | Major deliverable and exit gate |
| --- | --- | --- | --- |
| [1 UI](PHASE_01_UI.md) | Owner-completed; browser QA pending | None | Navigable demo, responsive UI, honest mock labels, successful build |
| [2 Backend](PHASE_02_BACKEND.md) | Implemented, browser QA pending | Phase 1 contracts | Authenticated owned sessions, records, analytics, API integration, test Mongo verification |
| [3 CV](PHASE_03_COMPUTER_VISION.md) | ACTIVE, device evaluation pending | Phase 2 records and consent model | Opt-in local processing and derived visual signals; validation before attention claims |
| [4 Intelligence](PHASE_04_AI_PERSONALIZATION.md) | Upcoming | Sufficient valid Phase 2/3 data | Calibrated baseline, explainable plans, coach, gamification |
| [5 Integration](PHASE_05_INTEGRATION_DEPLOYMENT.md) | Upcoming | Phases 2–4 | End-to-end, security/privacy checks, deployment |

## Current progress and next tasks

Phase 2 implemented FastAPI, MongoDB, JWT accounts, owned sessions, digital records, analytics, and recorded frontend views. Phase 3 now has an opt-in browser camera prototype, separate derived visual records, consent endpoints, and a provisional visual-signal index. Validated visual attention and focused-time estimates are still unavailable. Next: run real-camera, responsive, performance, and privacy-network QA; close the pending Phase 2 browser checks.

## Cross-phase acceptance and testing

Each phase needs documented API/data contracts, validation, authorization where applicable, tests for business rules and failure paths, build/start commands, and evidence for real integrations. Mock output is never evidence that a camera, AI model, or reward engine works. See each phase document for its gate.

## Known risks

- FlowFocus thresholds are unvalidated heuristics; copy only with attribution and adaptation.
- Client-reported digital activity and distractions can be forged; do not treat them as verified attention.
- The current frontend is a monolithic React component with local fixtures; its data-access seam needs care to preserve the presentation flow.
- The local MongoDB test passed, but staging/deployed MongoDB has not been verified.
- The Phase 1 build warns about a large JavaScript bundle; optimize only after the live flow is stable.

