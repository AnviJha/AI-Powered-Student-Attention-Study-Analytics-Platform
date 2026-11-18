# Mock Data and UI Contracts

## Purpose

Provide consistent demo data for the presentation while backend and AI services are not yet implemented.

## Rules

- Keep mock data in a central module or small set of fixture files.
- Components should consume stable object shapes rather than embedding unrelated literals.
- Use consistent units: durations in seconds or minutes internally, formatted for display.
- Use ISO timestamps for dates if dates are included.
- Clearly label fabricated analytics as demo/simulated.
- Do not persist sensitive webcam data.
- Do not add API calls in Phase 1 unless the repository already has a harmless mock API pattern.

## Suggested dashboard fixture

```js
export const dashboardSummary = {
  estimatedAttention: 82,
  focusedMinutes: 204,
  distractionCount: 8,
  currentStreakDays: 7,
  personalBaseline: 74,
  dailyGoalMinutes: 240,
  completedGoalMinutes: 204
};
```

## Suggested attention time series

```js
export const attentionSeries = [
  { time: "09:00", score: 76 },
  { time: "09:15", score: 81 },
  { time: "09:30", score: 84 },
  { time: "09:45", score: 78 },
  { time: "10:00", score: 71 },
  { time: "10:15", score: 80 }
];
```

## Suggested weekly study series

```js
export const weeklyStudySeries = [
  { day: "Mon", studyMinutes: 180, focusedMinutes: 142 },
  { day: "Tue", studyMinutes: 220, focusedMinutes: 176 },
  { day: "Wed", studyMinutes: 150, focusedMinutes: 111 },
  { day: "Thu", studyMinutes: 260, focusedMinutes: 214 },
  { day: "Fri", studyMinutes: 195, focusedMinutes: 158 },
  { day: "Sat", studyMinutes: 120, focusedMinutes: 91 },
  { day: "Sun", studyMinutes: 205, focusedMinutes: 164 }
];
```

## Suggested distraction categories

```js
export const distractionBreakdown = [
  { type: "Looking away", count: 5 },
  { type: "Face not detected", count: 2 },
  { type: "Phone detected (simulated)", count: 1 }
];
```

## Suggested recent sessions

```js
export const recentSessions = [
  {
    id: "demo-session-1",
    subject: "Machine Learning",
    topic: "Neural Networks",
    startedAt: "2026-11-18T07:00:00+05:30",
    durationMinutes: 50,
    focusedMinutes: 41,
    averageAttention: 83,
    distractionCount: 3
  },
  {
    id: "demo-session-2",
    subject: "Database Systems",
    topic: "Indexing",
    startedAt: "2026-11-17T18:30:00+05:30",
    durationMinutes: 45,
    focusedMinutes: 36,
    averageAttention: 79,
    distractionCount: 4
  }
];
```

## Suggested AI coach demo insight

```js
export const coachInsight = {
  title: "Your strongest sample focus window",
  summary: "Your demo study history shows stronger estimated attention in the evening.",
  recommendation: "Try scheduling a demanding topic during your preferred evening study window.",
  suggestedSessionMinutes: 45,
  suggestedBreakMinutes: 10,
  explanation: "This is a sample recommendation based on presentation data, not a live model."
};
```

## Suggested gamification fixture

```js
export const gamification = {
  level: 12,
  levelName: "Focus Builder",
  totalXp: 2340,
  xpIntoLevel: 340,
  xpToNextLevel: 660,
  currentStreakDays: 7,
  bestStreakDays: 12,
  badges: [
    { id: "first-focus", name: "First Focus", earned: true },
    { id: "week-warrior", name: "Week Warrior", earned: true },
    { id: "deep-work", name: "Deep Work", earned: false },
    { id: "goal-crusher", name: "Goal Crusher", earned: false }
  ]
};
```

## Future API boundary

When Phase 2 begins, replace fixture imports with API/service calls behind a small data-access layer. Keep UI components independent of whether the data comes from fixtures or FastAPI.
