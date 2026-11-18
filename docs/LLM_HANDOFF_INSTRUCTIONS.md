# LLM / Coding Agent Handoff Instructions

Read `README.md`, `docs/MASTER_CONTEXT.md`, `docs/UI_REQUIREMENTS.md`, `docs/DESIGN_SYSTEM.md`, `docs/MOCK_DATA_AND_UI_CONTRACTS.md`, `docs/ARCHITECTURE_AND_PHASES.md`, `docs/CODEX_HANDOFF.md`, `docs/ACCEPTANCE_CRITERIA.md`, `docs/OPEN_DECISIONS.md`, and `TODO.md` before making changes.

## Project understanding

This is a privacy-first student study companion. Its intended full product combines study-session tracking, webcam-derived behavioral signals, estimated attention, distraction analytics, personal baselines, study-pattern analysis, GenAI recommendations, and gamification.

## Current priority

Only Phase 1 is active: **complete frontend UI development for a presentation**. Build the full navigable UI with mock data. Do not implement the backend, database, webcam analysis, ML models, real LLM calls, or browser extension in this phase.

## Non-negotiable principles

- Inspect actual source code before editing.
- Do not assume planned features are implemented.
- Preserve existing working functionality and conventions.
- Do not fabricate API endpoints or database schemas as if they already exist.
- Label simulated metrics and insights.
- Say “estimated attention,” not “true attention.”
- Do not request or store webcam footage for a mock UI.
- Use one consistent mock-data source.
- Avoid unnecessary rewrites and dependencies.
- Verify with the repository's actual build/test commands.
- Update TODO and documentation when meaningful work is completed.

## Continuation rule

When Phase 1 is complete, stop and report the UI completion status. Do not automatically begin Phase 2. Wait for the project owner to authorize the next phase.
