# Codex Development Handoff

You are the implementation agent for the AI-Powered Student Attention & Study Analytics Platform.

## First instruction

**Work only on Phase 1: complete UI development for an upcoming presentation.** Do not start backend, database, real computer vision, machine learning, or real GenAI integration.

## Before coding

1. Inspect the repository root, package manifest, lockfile, existing source structure, and current app entry points.
2. Identify the framework version, package manager, scripts, styling setup, and existing component conventions.
3. Run the existing app/build if possible to establish a baseline.
4. Preserve existing working code and visual components where reasonable.
5. If the repository is empty, initialize the simplest suitable React setup consistent with the stated stack; explain the choice in the final report.

## Required UI scope

Implement the screens and interactions in `UI_REQUIREMENTS.md`:
- Dashboard
- Study Session
- Analytics (daily/weekly/monthly)
- AI Study Coach
- Goals & Challenges
- Achievements / Gamification
- Profile / Settings

Build shared layout/navigation and reusable components. Ensure navigation works and the UI is responsive.

## Data and simulation

- Use centralized, realistic mock data based on `MOCK_DATA_AND_UI_CONTRACTS.md`.
- Use local state for demo interactions such as starting/pausing/ending a session and completing a challenge.
- No real API calls are required.
- No real LLM calls are required.
- Do not request webcam permission merely to make the demo look complete.
- Any simulated attention, phone detection, camera state, recommendations, and analytics must be clearly presented as demo/simulated.

## Technical constraints

- Prefer the repository's existing stack and package manager.
- Use React and Tailwind if already configured or configure them with minimal disruption.
- Use Recharts for charts if installed or add it only if compatible with the current setup.
- Keep components modular and readable.
- Avoid unnecessary dependencies.
- Do not hardcode different conflicting metrics across screens; use shared fixtures.
- Do not add secrets or real API keys.
- Do not implement backend folders/services in this phase unless they already exist and must remain untouched.

## Definition of done

- All primary screens can be opened from navigation.
- Primary buttons and controls have meaningful demo behavior.
- Charts render from centralized mock data.
- UI is responsive at desktop/tablet/mobile widths.
- No major console errors or broken routes.
- Existing build/dev commands work.
- Demo-only behavior is labeled honestly.
- Provide a concise summary of files changed, commands run, build/test result, and any remaining UI gaps.

## Working style

- Make small, coherent changes.
- Inspect before modifying.
- Do not rewrite the whole project without need.
- If a critical design choice is ambiguous, choose a restrained, consistent default and document it; ask the project owner only if it blocks implementation.
- Update `TODO.md` as Phase 1 tasks are completed.
- Do not mark future phases complete merely because their UI is represented with mock data.
