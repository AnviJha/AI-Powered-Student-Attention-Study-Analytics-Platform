import React, { useEffect, useState } from 'react'
import { api } from './api'
import VisualMonitor from './VisualMonitor'

export default function LiveWorkspace({ screen = 'live', enabled = true }) {
  const [token, setToken] = useState('')
  const [mode, setMode] = useState('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [subject, setSubject] = useState('')
  const [topic, setTopic] = useState('')
  const [profile, setProfile] = useState(null)
  const [sessions, setSessions] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [plan, setPlan] = useState(null)
  const [period, setPeriod] = useState('daily')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [profileName, setProfileName] = useState('')
  const [profileGoal, setProfileGoal] = useState(240)
  const [profileZone, setProfileZone] = useState('UTC')
  const [profilePreferred, setProfilePreferred] = useState(45)
  const [profileNotifications, setProfileNotifications] = useState(true)

  async function refresh(auth = token, selected = period) {
    setLoading(true); setError('')
    try {
      const [p, s, a, f] = await Promise.all([
        api('/api/profile', {token: auth}), api('/api/sessions', {token: auth}),
        api(`/api/analytics?period=${selected}`, {token: auth}), api('/api/focus/plan', {token: auth}),
      ])
      setProfile(p); setProfileName(p.name); setProfileGoal(p.daily_goal_minutes); setProfileZone(p.time_zone || 'UTC'); setProfilePreferred(p.preferred_session_minutes); setProfileNotifications(p.notifications_enabled); setSessions(s); setAnalytics(a); setPlan(f)
    } catch (e) { setError(e.message) } finally { setLoading(false) }
  }
  useEffect(() => { if (token) refresh(token, period) }, [period])
  async function submitAuth(e) {
    e.preventDefault(); setLoading(true); setError('')
    try {
      const result = await api(`/api/auth/${mode}`, {method:'POST', body: mode==='register' ? {name,email,password} : {email,password}})
      setToken(result.access_token); setPassword(''); await refresh(result.access_token)
    } catch (e) { setError(e.message) } finally { setLoading(false) }
  }
  async function start(e) {
    e.preventDefault(); setLoading(true); setError('')
    try { await api('/api/sessions', {token, method:'POST', body:{subject,topic,goal_minutes:45}}); setSubject(''); setTopic(''); await refresh() }
    catch(e) { setError(e.message) } finally { setLoading(false) }
  }
  async function change(id, action) {
    setLoading(true); setError('')
    try { await api(`/api/sessions/${id}/status/${action}`, {token,method:'POST'}); await refresh() }
    catch(e) { setError(e.message) } finally { setLoading(false) }
  }
  async function deleteVisual(id) {
    if (!window.confirm('Delete all derived visual records for this session?')) return
    setError('')
    try { await api(`/api/sessions/${id}/visual-records`, {token, method:'DELETE'}); await refresh() }
    catch(e) { setError(e.message) }
  }
  async function saveProfile(e) {
    e.preventDefault(); setLoading(true); setError('')
    try {
      await api('/api/profile', {token, method:'PATCH', body:{name:profileName, daily_goal_minutes:Number(profileGoal), preferred_session_minutes:Number(profilePreferred), notifications_enabled:profileNotifications, time_zone:profileZone}})
      await refresh()
    } catch(e) { setError(e.message) } finally { setLoading(false) }
  }
  return <div className="live-workspace">
    <div className="privacy"><span>⌑</span><div><strong>Recorded data workspace · Phase 3</strong><p>Digital engagement is a heuristic. Optional visual signals run locally in your browser; their index is provisional and distinct from validated visual attention. Estimated focused time remains unavailable.</p></div></div>
    {error && <div className="info-message error" role="alert">{error}</div>}
    {!token ? <section className="card live-auth"><h2>{mode==='login'?'Sign in':'Create account'}</h2><p className="muted">Connect to the local FastAPI backend. Your token stays in memory and clears on reload.</p><form onSubmit={submitAuth}>
      {mode==='register'&&<label>Name<input value={name} onChange={e=>setName(e.target.value)} required minLength="1"/></label>}
      <label>Email<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></label>
      <label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} required minLength={mode==='register'?10:1}/></label>
      <button className="primary" disabled={loading}>{loading?'Connecting…':mode==='login'?'Sign in':'Register'}</button>
    </form><button className="text-button" onClick={()=>setMode(mode==='login'?'register':'login')}>{mode==='login'?'Create an account':'Use an existing account'}</button></section> : <>
      <div className="live-toolbar"><strong>{profile?.name || 'Student'} · recorded workspace</strong><button className="secondary" onClick={()=>{setToken('');setProfile(null);setSessions([]);setAnalytics(null);setPlan(null)}}>Sign out</button></div>
      {(screen==='session'||screen==='live')&&<div className="two-col"><section className="card"><div className="card-head"><h2>Start a recorded session</h2></div><form onSubmit={start} className="live-form"><label>Subject<input value={subject} onChange={e=>setSubject(e.target.value)} required/></label><label>Topic<input value={topic} onChange={e=>setTopic(e.target.value)}/></label><button className="primary" disabled={loading||!subject.trim()}>Start session</button></form></section><section className="card"><div className="card-head"><h2>Focus plan</h2></div>{plan?<><div className="goal-big">{plan.focus_minutes} min <span>study / {plan.break_minutes} min break</span></div><p className="muted">{plan.reasons.join(' ')} Source: {plan.score_source.replace('_',' ')} · {plan.confidence} sample confidence · provisional heuristic.</p></>:<p className="muted">{loading?'Loading…':'No plan available.'}</p>}</section></div>}
      {(screen==='analytics'||screen==='dashboard'||screen==='live')&&<section className="card live-section"><div className="card-head"><h2>Recorded analytics</h2><select aria-label="Analytics period" value={period} onChange={e=>setPeriod(e.target.value)}><option value="daily">Daily</option><option value="weekly">Weekly</option><option value="monthly">Monthly</option></select></div>{analytics?<><div className="live-metrics"><div><strong>{analytics.session_count}</strong><span>sessions</span></div><div><strong>{Math.round(analytics.study_seconds/60)} min</strong><span>study time</span></div><div><strong>{analytics.average_digital_engagement_score == null?'Unavailable':`${analytics.average_digital_engagement_score}%`}</strong><span>avg. digital engagement</span></div><div><strong>{analytics.average_visual_attention_score == null?'Unavailable':`${analytics.average_visual_attention_score}%`}</strong><span>avg. visual attention</span></div><div><strong>{analytics.potential_distraction_count}</strong><span>client-reported potential distractions</span></div></div>{analytics.by_day?.length>0&&<div className="live-days">{analytics.by_day.map(day=><div key={day.date}><span>{day.date}</span><strong>{Math.round(day.study_seconds/60)} min study</strong></div>)}</div>}</>:<p className="muted">{loading?'Loading…':'Analytics unavailable.'}</p>}</section>}
      {(screen==='session'||screen==='dashboard'||screen==='live')&&<section className="card live-section"><div className="card-head"><h2>Recorded sessions</h2><button className="text-button" onClick={()=>refresh()} disabled={loading}>Refresh ↻</button></div>{sessions.length===0?<div className="empty"><h3>No recorded sessions yet</h3><p>Start one in Study session. Demo sessions are separate.</p></div>:<div className="session-list">{sessions.map(s=><div className="session-row" key={s.id}><span className="subject-icon">▤</span><span className="row-main"><strong>{s.subject}</strong><small>{s.topic || 'Open study block'} · {s.status}</small></span><span className="row-metric">{Math.round(s.active_seconds/60)} min<small>recorded</small></span>{s.status!=='ended'&&<div className="live-actions">{s.status==='active'?<button className="secondary" disabled={loading} onClick={()=>change(s.id,'pause')}>Pause</button>:<button className="secondary" disabled={loading} onClick={()=>change(s.id,'resume')}>Resume</button>}<button className="danger-button" disabled={loading} onClick={()=>change(s.id,'end')}>End</button></div>}{s.status!=='active'&&<button className="text-button" onClick={()=>deleteVisual(s.id)}>Delete visual data</button>}</div>)}</div>}</section>}
      {enabled && (screen==='session'||screen==='live') && sessions.filter(s=>s.status==='active').map(s=><VisualMonitor key={s.id} sessionId={s.id} token={token}/>)}
      {(screen==='settings'||screen==='live')&&<section className="card live-section"><div className="card-head"><h2>Recorded profile</h2></div><form className="live-form" onSubmit={saveProfile}><label>Name<input value={profileName} onChange={e=>setProfileName(e.target.value)} required/></label><label>Daily goal (minutes)<input type="number" min="30" max="720" value={profileGoal} onChange={e=>setProfileGoal(e.target.value)} required/></label><label>Preferred session length (minutes)<input type="number" min="10" max="180" value={profilePreferred} onChange={e=>setProfilePreferred(e.target.value)} required/></label><label>Time zone<select value={profileZone} onChange={e=>setProfileZone(e.target.value)}><option value="UTC">UTC</option><option value="Asia/Kolkata">Asia/Kolkata</option><option value="Europe/London">Europe/London</option><option value="America/New_York">America/New_York</option></select></label><label className="live-check"><input type="checkbox" checked={profileNotifications} onChange={e=>setProfileNotifications(e.target.checked)}/> Notification preference (no messages are sent yet)</label><button className="primary" disabled={loading}>Save profile</button></form></section>}
    </>}
  </div>
}
