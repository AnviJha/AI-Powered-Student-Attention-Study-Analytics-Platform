# Open Decisions and Unknowns

The following details were not established by the project discussion or a source-code inspection. Codex should inspect the repository and avoid inventing facts.

1. **Existing repository state:** No source-code tree was provided. Framework version, current components, routes, scripts, and dependencies are unknown.
2. **Branding:** “FocusAI” appeared as an illustrative name in an earlier dashboard concept, but the final product name/logo is not confirmed.
3. **Visual theme:** A modern dashboard was requested, but final light/dark theme, exact palette, and font are not locked. Choose a consistent presentation-ready direction unless the repository already defines one.
4. **User identity:** Use a neutral demo student profile. Do not assume a real name or personal data.
5. **Exact metric formulas:** Attention score, focused-time threshold, focus efficiency, and streak qualification rules are not scientifically or technically finalized. For Phase 1, show illustrative demo values and avoid presenting formulas as validated.
6. **Camera UX:** The eventual permission and processing flow is not finalized. Phase 1 must not request webcam access just to show a mock interface.
7. **GenAI provider:** Gemini or OpenAI is under consideration; neither is selected. No provider integration in Phase 1.
8. **Prediction approach:** No training dataset, target definition, evaluation metric, or model is available. Prediction is future scope.
9. **Gamification economy:** XP values, level thresholds, and challenge rules are examples only and require product validation before backend implementation.
10. **Deployment target:** Vercel/Render/Railway are candidates, not confirmed deployments.

## Evidence checked

- Project requirements and feature descriptions in the conversation.
- Uploaded `Pasted markdown.md`, which is a generic project handoff documentation prompt and does not contain this project's source code or implementation evidence.

## Owner input needed later

These decisions do not block Phase 1 if Codex uses reasonable defaults:
- Final product branding.
- Preferred light or dark theme.
- Exact presentation/demo user persona.
- Which screen should be the first landing page.
