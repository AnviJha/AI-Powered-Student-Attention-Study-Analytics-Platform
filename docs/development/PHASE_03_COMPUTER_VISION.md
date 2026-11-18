# Phase 03 — Computer vision and visual signals

## Objective and status

**ACTIVE; browser/device validation pending.** Add optional browser-local camera signals to owned recorded sessions. The implementation is a provisional face-presence and head-orientation *proxy*. It does not measure comprehension, mental focus, gaze, or validated visual attention. Phase 2 authenticated sessions and MongoDB are prerequisites. The Phase 2 responsive browser QA item remains open.

## Scope and implementation order

1. Show an opt-in control only for an active recorded session. Request browser camera permission after the student clicks it. The demo mode never requests a camera.
2. Load the bundled MediaPipe Face Landmarker model and WASM assets in the browser. Sample at approximately 2 Hz and aggregate 10-second windows. Keep frames and landmarks in memory only.
3. Estimate face presence and a coarse forward head-orientation proxy from nose and eye landmarks. Count unusable samples separately. Do not infer eye gaze, blink, phone use, or distraction from this prototype.
4. Register server-side visual consent; submit only nested sample counts and an algorithm version. FastAPI calculates the provisional index. Consent is revoked on stop; pausing or ending the session also clears it server-side.
5. Store derived visual windows in a separate MongoDB collection with a 90-day TTL index. Offer earlier per-session deletion. Keep digital engagement records, validated visual attention, and combined engagement separate.
6. Evaluate accuracy, usability, CPU cost, lighting, eyewear, skin tones, and device variation with consented participants before treating any threshold as reliable.

## Relevant files and dependencies

- `src/VisualMonitor.jsx`: opt-in UI, local preview, stream and inference lifecycle.
- `src/visualSignals.js`: count aggregation and coarse orientation proxy.
- `public/mediapipe/`: bundled Google model and WASM runtime. See [asset provenance](../MEDIAPIPE_ASSETS.md) for source, version, checksum, and license boundary.
- `backend/app/services/visual.py`: versioned provisional index and missing-quality behavior.
- `backend/app/main.py`: consent and visual-record endpoints, owned-session checks, TTL index.
- `backend/tests/test_visual.py`, `src/visualSignals.test.js`: deterministic rule and API tests.

No Python OpenCV, YOLO, or GenAI dependency is needed for browser-local Phase 3. Camera access requires a browser secure context (HTTPS or localhost) and student permission.

## API and database contract

All endpoints require the existing Bearer JWT and an owned session. `POST /api/sessions/{id}/visual-consent` requires an active session. `DELETE /api/sessions/{id}/visual-consent` revokes submission authorization. Pausing or ending the session also revokes it.

`POST /api/sessions/{id}/visual-records` requires active consent and accepts only `algorithm_version`, `total_samples`, `valid_samples`, `face_samples`, and `forward_samples`. Counts are bounded to 0–50 and must be nested. The server timestamps the record, calculates `visual_signal_index`, sets quality and explanations, and enforces an eight-second minimum between windows. It does not accept a client-supplied score or image. `GET` lists up to 100 recent windows; `DELETE` removes all visual windows for the owned session. MongoDB `visual_records.expires_at` has a 90-day expiry index. Existing digital records are not migrated or reinterpreted.

The index is `round(100 × (0.4 × face_samples/valid_samples + 0.6 × forward_samples/valid_samples))`. It is `null` when fewer than five valid samples or less than half the samples are usable. The coefficients and geometry bounds are provisional engineering heuristics, not validated scientific thresholds. `visual_attention_score`, `combined_study_engagement`, and `estimated_focused_seconds` remain `null` until later validation and calibration.

## Integration and privacy

The camera is stopped on explicit stop, route or mode change, tab hiding, pause/end, sign-out, or component cleanup. A server consent flag alone cannot prove that a browser is capturing; a browser client can forge count payloads, so these records must not grant rewards or carry clinical claims. Raw frames, landmarks, and video are not sent to the API or persisted. The source model and WASM are loaded from this app's own static assets. When a record submission fails, monitoring stops and an error is shown.

## Testing and acceptance

Automated: test scoring and unknown quality; nested-count and arbitrary-score rejection; user ownership; missing consent; revocation; pause; rate limiting; per-session deletion; 90-day expiry value; frontend geometry and count aggregation; production build. Existing Phase 2 backend tests must continue passing.

Manual acceptance still required: test permission denial, missing camera, camera disconnect, browser tab hide, pause/end while capturing, mobile/tablet layout, 10-second record creation against local MongoDB, and no frame payloads in network requests. Record inference latency and CPU load on at least a typical laptop and mobile browser. Conduct a consented labeled evaluation across lighting, eyewear, skin tones, and posture before promoting the index to visual-attention analytics. Optional YOLO phone detection and eye/gaze signals need separate feasibility and privacy review.

## Known risks and completion checklist

Face visibility can fail for ordinary study posture, lighting, occlusion, camera placement, or assistive use. Coarse facial geometry is not calibrated head pose. The current index is not suitable for student ranking, grades, or punitive alerts. The bundled model and WASM add substantial static asset size. Review model distribution terms before deployment.

- [x] Opt-in permission and revoke UX implemented in recorded sessions.
- [x] Browser-local face-presence and coarse orientation prototype implemented.
- [x] Owned derived-signal API, validation, consent, deletion, and 90-day expiry implemented.
- [x] Deterministic service/API and frontend signal tests added.
- [ ] Real-camera, responsive, performance, and privacy-network manual QA recorded.
- [ ] Consented labeled evaluation and fairness review completed.
- [ ] Eye/gaze and optional phone-detection feasibility documented with evidence.
