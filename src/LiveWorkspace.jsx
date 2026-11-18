import React, { useEffect, useState } from 'react'
import { api } from './api'

export default function LiveWorkspace() {
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

  async function refresh(auth = token, selected = period) {
    setLoading(true); setError('')
    try {
      const [p, s, a, f] = await Promise.all([
        api('/api/profile', {token: auth}), api('/api/sessions', {token: auth}),
        api(`/api/analytics?period=${selected}`, {token: auth}), api('/api/focus/plan', {token: auth}),
      ])
      setProfile(p); setSessions(s); setAnalytics(a); setPlan(f)
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
  return <div className="live-workspace">
    <div className="privacy"><span>⌑</span><div><strong>Recorded data workspace · Phase 2</strong><p>This view uses the local backend. Digital engagement is a heuristic; visual attention and estimated focused time are unavailable until a validated visual-signal pipeline exists. No camera or AI provider is used.</p></div></div>
    {error && <div className="info-message error" role="alert">{error}</div>}
    {!token ? <section className="card live-auth"><h2>{mode==='login'?'Sign in':'Create account'}</h2><p className="muted">Connect to the local FastAPI backend. Your token stays in memory and clears on reload.</p><form onSubmit={submitAuth}>
      {mode==='register'&&<label>Name<input value={name} onChange={e=>setName(e.target.value)} required minLength="1"/></label>}
      <label>Email<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required/></label>
      <label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} required minLength={mode==='register'?10:1}/></label>
      <button className="primary" disabled={loading}>{loading?'Connecting…':mode==='login'?'Sign in':'Register'}</button>
    </form><button className="text-button" onClick={()=>setMode(mode==='login'?'register':'login')}>{mode==='login'?'Create an account':'Use an existing account'}</button></section> : <>
      <div className="live-toolbar"><strong>{profile?.name || 'Student'} · recorded workspace</strong><button className="secondary" onClick={()=>{setToken('');setProfile(null);setSessions([]);setAnalytics(null);setPlan(null)}}>Sign out</button></div>
      <div className="two-col"><section className="card"><div className="card-head"><h2>Start a recorded session</h2></div><form onSubmit={start} className="live-form"><label>Subject<input value={subject} onChange={e=>setSubject(e.target.value)} required/></label><label>Topic<input value={topic} onChange={e=>setTopic(e.target.value)}/></label><button className="primary" disabled={loading||!subject.trim()}>Start session</button></form></section><section className="card"><div className="card-head"><h2>Focus plan</h2></div>{plan?<><div className="goal-big">{plan.focus_minutes} min <span>study / {plan.break_minutes} min break</span></div><p className="muted">{plan.reasons.join(' ')} Source: {plan.score_source.replace('_',' ')} · {plan.confidence} sample confidence · provisional heuristic.</p></>:<p className="muted">{loading?'Loading…':'No plan available.'}</p>}</section></div>
      <section className="card live-section"><div className="card-head"><h2>Recorded analytics</h2><select aria-label="Analytics period" value={period} onChange={e=>setPeriod(e.target.value)}><option value="daily">Daily</option><option value="weekly">Weekly</option><option value="monthly">Monthly</option></select></div>{analytics?<div className="live-metrics"><div><strong>{analytics.session_count}</strong><span>sessions</span></div><div><strong>{Math.round(analytics.study_seconds/60)} min</strong><span>study time</span></div><div><strong>{analytics.average_digital_engagement_score == null?'Unavailable':`${analytics.average_digital_engagement_score}%`}</strong><span>avg. digital engagement</span></div><div><strong>{analytics.average_visual_attention_score == null?'Unavailable':`${analytics.average_visual_attention_score}%`}</strong><span>avg. visual attention</span></div><div><strong>{analytics.potential_distraction_count}</strong><span>client-reported potential distractions</span></div></div>:<p className="muted">{loading?'Loading…':'Analytics unavailable.'}</p>}</section>
      <section className="card live-section"><div className="card-head"><h2>Recorded sessions</h2><button className="text-button" onClick={()=>refresh()} disabled={loading}>Refresh ↻</button></div>{sessions.length===0?<div className="empty"><h3>No recorded sessions yet</h3><p>Start one above. Demo sessions on the presentation screens are separate.</p></div>:<div className="session-list">{sessions.map(s=><div className="session-row" key={s.id}><span className="subject-icon">▤</span><span className="row-main"><strong>{s.subject}</strong><small>{s.topic || 'Open study block'} · {s.status}</small></span><span className="row-metric">{Math.round(s.active_seconds/60)} min<small>recorded</small></span>{s.status!=='ended'&&<div className="live-actions">{s.status==='active'?<button className="secondary" disabled={loading} onClick={()=>change(s.id,'pause')}>Pause</button>:<button className="secondary" disabled={loading} onClick={()=>change(s.id,'resume')}>Resume</button>}<button className="danger-button" disabled={loading} onClick={()=>change(s.id,'end')}>End</button></div>}</div>)}</div>}</section>
    </>}
  </div>
}
