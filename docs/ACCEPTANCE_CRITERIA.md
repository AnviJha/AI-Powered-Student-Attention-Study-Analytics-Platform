# Phase 1 Acceptance Criteria

Phase 1 is complete only when the presentation UI meets the following criteria.

## Application shell
- [ ] App loads without runtime errors.
- [ ] Sidebar/navigation is consistent across screens.
- [ ] Every primary navigation destination works.
- [ ] Layout adapts to desktop, tablet, and mobile.

## Dashboard
- [ ] Greeting and primary start-session action are visible.
- [ ] Summary metrics are coherent and use shared mock data.
- [ ] Attention and weekly study charts render.
- [ ] Baseline, coach insight, daily goal, and recent sessions are represented.

## Study Session
- [ ] Student can start a demo session.
- [ ] Student can pause and resume.
- [ ] Student can end the demo session.
- [ ] Session metrics and events are clearly simulated.
- [ ] No camera permission is requested unless real camera functionality is separately approved.

## Analytics
- [ ] Daily, weekly, and monthly period selection works.
- [ ] Relevant metrics and charts update or switch with the selected period.
- [ ] Empty state is available for a no-history scenario.

## AI Study Coach
- [ ] Demo insight and recommendations are visible.
- [ ] Recommendation includes a reason/context.
- [ ] No real LLM call is made in Phase 1.

## Goals and gamification
- [ ] Goal progress is visible.
- [ ] Challenge completion can be demonstrated.
- [ ] XP/level progress is visible.
- [ ] Streak and badges have earned/locked states.
- [ ] Demo reward updates are coherent if interactive.

## Trust and privacy
- [ ] Demo data is labeled.
- [ ] Estimated attention terminology is used.
- [ ] Privacy explanation is visible.
- [ ] UI does not claim that mental attention is directly measured.
- [ ] Raw webcam video is neither requested nor stored for the UI-only demo.

## Build and demo readiness
- [ ] Existing development command starts the application.
- [ ] Production build succeeds.
- [ ] No major broken layout, dead button, or horizontal overflow.
- [ ] Presentation flow can be completed without backend connectivity.
