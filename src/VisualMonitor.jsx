import React, { useEffect, useRef, useState } from 'react'
import { api } from './api'
import { addSample, emptyWindow } from './visualSignals'

export default function VisualMonitor({ sessionId, token }) {
  const video = useRef(null)
  const runtime = useRef(null)
  const [state, setState] = useState('off')
  const [message, setMessage] = useState('Camera is off. Start monitoring only if you want local visual-signal estimates.')
  const [latest, setLatest] = useState(null)
  const [records, setRecords] = useState([])

  function cleanup(revoke = true) {
    const old = runtime.current
    runtime.current = null
    if (!old) return
    clearInterval(old.sampleTimer)
    clearInterval(old.uploadTimer)
    old.stream?.getTracks().forEach(track => track.stop())
    old.landmarker?.close()
    if (video.current) video.current.srcObject = null
    if (revoke && old.consented) api(`/api/sessions/${sessionId}/visual-consent`, { token, method: 'DELETE' }).catch(() => {})
  }

  useEffect(() => {
    api(`/api/sessions/${sessionId}/visual-records`, { token }).then(items => { setRecords(items); setLatest(items[0] || null) }).catch(() => {})
    return () => cleanup()
  }, [sessionId, token])

  useEffect(() => {
    const onHidden = () => {
      if (document.hidden && runtime.current) { cleanup(); setState('off'); setMessage('Monitoring stopped when this tab became hidden.') }
    }
    document.addEventListener('visibilitychange', onHidden)
    return () => document.removeEventListener('visibilitychange', onHidden)
  }, [sessionId, token])

  async function start() {
    if (runtime.current || state === 'starting') return
    if (!navigator.mediaDevices?.getUserMedia) { setState('error'); setMessage('Camera access requires a supported browser and a secure context such as localhost or HTTPS.'); return }
    setState('starting'); setMessage('Requesting camera permission and loading the local face model…')
    const run = { stream: null, landmarker: null, sampleTimer: null, uploadTimer: null, consented: false, window: emptyWindow() }
    runtime.current = run
    try {
      run.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }, audio: false })
      if (runtime.current !== run) { run.stream.getTracks().forEach(track => track.stop()); return }
      if (video.current) { video.current.srcObject = run.stream; await video.current.play() }
      if (runtime.current !== run) return
      const { FaceLandmarker, FilesetResolver } = await import('@mediapipe/tasks-vision')
      const fileset = await FilesetResolver.forVisionTasks('/mediapipe/wasm')
      run.landmarker = await FaceLandmarker.createFromOptions(fileset, {
        baseOptions: { modelAssetPath: '/mediapipe/face_landmarker.task', delegate: 'CPU' },
        runningMode: 'VIDEO', numFaces: 1,
      })
      if (runtime.current !== run) { run.landmarker.close(); return }
      await api(`/api/sessions/${sessionId}/visual-consent`, { token, method: 'POST' })
      run.consented = true
      setState('on'); setMessage('Local monitoring is on. Only 10-second sample counts leave this browser.')
      run.sampleTimer = setInterval(() => {
        if (runtime.current !== run) return
        if (!run.stream.getVideoTracks().some(track => track.readyState === 'live')) {
          cleanup(); setState('error'); setMessage('Camera signal was lost. Monitoring stopped.'); return
        }
        try {
          if (!video.current || video.current.readyState < 2) { addSample(run.window, null, false); return }
          const result = run.landmarker.detectForVideo(video.current, performance.now())
          addSample(run.window, result.faceLandmarks?.[0] || null)
        } catch { addSample(run.window, null, false) }
      }, 500)
      run.uploadTimer = setInterval(async () => {
        if (runtime.current !== run) return
        const payload = run.window
        run.window = emptyWindow()
        try {
          const result = await api(`/api/sessions/${sessionId}/visual-records`, { token, method: 'POST', body: payload })
          if (runtime.current === run) { setLatest(result); setRecords(previous => [result, ...previous].slice(0, 100)) }
        } catch (error) {
          if (runtime.current === run) { cleanup(); setState('error'); setMessage(`Monitoring stopped: ${error.message}`) }
        }
      }, 10000)
    } catch (error) {
      if (runtime.current !== run) return
      cleanup()
      setState('error')
      setMessage(error.name === 'NotAllowedError' ? 'Camera permission was denied. You can continue studying without monitoring.' : `Camera unavailable: ${error.message}`)
    }
  }

  function stop() { cleanup(); setState('off'); setMessage('Monitoring stopped. Previously saved derived records remain until deleted or their 90-day expiry.') }
  async function deleteRecords() {
    if (!window.confirm('Delete all derived visual records for this session?')) return
    try { await api(`/api/sessions/${sessionId}/visual-records`, { token, method: 'DELETE' }); setRecords([]); setLatest(null); setMessage('This session’s derived visual records were deleted.') }
    catch (error) { setMessage(`Could not delete records: ${error.message}`) }
  }

  return <section className="card live-section visual-monitor"><div className="card-head"><h2>Optional camera signals</h2><span className="pill">{state === 'on' ? 'Monitoring on' : 'Camera off'}</span></div>
    <p className="muted">Face presence and coarse head orientation are estimated on this device. This provisional index does not measure learning or mental focus. No video or facial landmarks are uploaded.</p>
    <video ref={video} autoPlay muted playsInline className="visual-preview" aria-label="Local camera preview" />
    <p role="status" className="muted">{message}</p>
    <div className="visual-actions">{state === 'on' || state === 'starting' ? <button className="secondary" onClick={stop}>Stop monitoring</button> : <button className="primary" onClick={start}>Start optional monitoring</button>}
      <button className="danger-button" onClick={deleteRecords} disabled={!records.length}>Delete derived records</button></div>
    <div className="visual-result"><strong>{latest?.visual_signal_index == null ? 'No usable visual signal yet' : `${latest.visual_signal_index}/100 provisional visual signal index`}</strong>
      {latest && <small>{latest.reasons.join(' · ')}</small>}<small>{records.length} saved window{records.length === 1 ? '' : 's'} · automatically expire after 90 days</small></div>
  </section>
}
