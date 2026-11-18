export const student = { name: 'Alex Morgan', initials: 'AM', program: 'Computer Science', year: 'Year 2' }
export const summary = { estimatedAttention: 82, focusedMinutes: 204, studyMinutes: 250, distractionCount: 8, currentStreakDays: 7, personalBaseline: 74, dailyGoalMinutes: 240 }
export const attentionSeries = [
  { time: '09:00', score: 76 }, { time: '09:15', score: 81 }, { time: '09:30', score: 84 },
  { time: '09:45', score: 78 }, { time: '10:00', score: 71 }, { time: '10:15', score: 80 },
  { time: '10:30', score: 86 }, { time: '10:45', score: 83 },
]
export const weeklyStudy = [
  { day: 'Mon', study: 180, focused: 142 }, { day: 'Tue', study: 220, focused: 176 },
  { day: 'Wed', study: 150, focused: 111 }, { day: 'Thu', study: 260, focused: 214 },
  { day: 'Fri', study: 195, focused: 158 }, { day: 'Sat', study: 120, focused: 91 },
  { day: 'Sun', study: 250, focused: 204 },
]
export const monthlyStudy = [
  { day: 'Week 1', study: 920, focused: 718 }, { day: 'Week 2', study: 1100, focused: 870 },
  { day: 'Week 3', study: 980, focused: 775 }, { day: 'Week 4', study: 1375, focused: 1096 },
]
export const distractions = [{ type: 'Looking away', count: 5 }, { type: 'Face not detected', count: 2 }, { type: 'Phone signal (simulated)', count: 1 }]
export const recentSessions = [
  { id: 's1', subject: 'Machine Learning', topic: 'Neural Networks', date: '2026-11-18T07:00:00+05:30', duration: 50, focused: 41, attention: 83, distractions: 3 },
  { id: 's2', subject: 'Database Systems', topic: 'Indexing', date: '2026-11-17T18:30:00+05:30', duration: 45, focused: 36, attention: 79, distractions: 4 },
  { id: 's3', subject: 'Linear Algebra', topic: 'Eigenvectors', date: '2026-11-16T09:15:00+05:30', duration: 60, focused: 49, attention: 81, distractions: 2 },
]
export const coach = { title: 'Your strongest sample focus window', summary: 'Your demo history shows stronger estimated attention in the evening.', recommendation: 'Try a demanding topic between 6:00 and 8:00 PM.', session: 45, break: 10, reason: 'The sample sessions in that window show fewer potential distractions. This is a suggestion based on presentation data.' }
export const challenges = [
  { id: 'morning', title: 'Intentional start', detail: 'Plan one focused session today', xp: 30 },
  { id: 'deep', title: 'Deep study block', detail: 'Complete a 45-minute study block', xp: 60 },
  { id: 'reflect', title: 'Reflect & reset', detail: 'Review your study pattern', xp: 20 },
]
export const game = { level: 12, levelName: 'Focus Builder', totalXp: 2340, levelXp: 340, nextLevelXp: 660, currentStreak: 7, bestStreak: 12,
  badges: [
    { name: 'First Focus', detail: 'Completed a first session', earned: true, icon: '✦' },
    { name: 'Week Warrior', detail: 'Seven-day goal streak', earned: true, icon: '◈' },
    { name: 'Deep Work', detail: 'Long, attentive session', earned: false, icon: '◆' },
    { name: 'Goal Crusher', detail: 'Meet several daily goals', earned: false, icon: '✳' },
    { name: 'Comeback', detail: 'Improve against baseline', earned: false, icon: '↗' },
  ],
  records: [{ label: 'Longest session', value: '72 min' }, { label: 'Best estimated attention', value: '91%' }, { label: 'Most focused day', value: '4h 12m' }],
}
export const minutes = n => `${Math.floor(n / 60)}h ${String(n % 60).padStart(2, '0')}m`
