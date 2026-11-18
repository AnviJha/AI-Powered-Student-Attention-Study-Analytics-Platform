# Phase 03 — Computer vision and attention detection

## Objective and status

Upcoming. Extract opt-in local visual signals while keeping raw frames out of persistent storage by default. Depends on Phase 2 authentication, owned sessions, and record contracts.

## Scope, features, and order

1. Add a clear webcam permission and revoke flow to the session UI; no capture before opt-in.
2. Prototype local OpenCV/MediaPipe face presence and head pose, then assess whether eye/gaze estimation is feasible under lighting, glasses, and device variation.
3. Define sampling frequency, timestamp, confidence, missing-signal states, and bounded retention for derived records. Do not retain raw frames or send them to GenAI.
4. Add explainable visual-attention and potential-distraction rules, with optional YOLO phone detection only after evaluating accuracy and resource cost.
5. Send only derived signals through a validated, owned API; distinguish visual, digital, and combined metrics. Never infer comprehension from face or gaze.

## Files, dependencies, APIs, database

Expected new local CV module and tests plus session UI consent controls; exact files are set after the prototype. OpenCV and MediaPipe are Phase 3 dependencies, YOLO optional. Extend the Phase 2 attention-record schema with consent/source/quality and derived-signal fields, not image blobs. Add revocation and deletion behavior. No database migration should silently reinterpret existing digital records as visual scores.

## Tests and acceptance

Test camera denial, no-device, signal loss, invalid quality, false positives, user revocation, and CPU use. Evaluate against a consented labeled sample before describing any threshold as reliable. Acceptance: no permission request before opt-in; no raw footage stored by default; valid derived records appear only for owned sessions; missing signals remain unknown.

## Risks and checklist

Lighting, skin tone, eyewear, posture, and device differences can affect estimates. Misleading scores and privacy loss are primary risks.

- [ ] Permission and revoke UX.
- [ ] Local signal prototype and evaluation.
- [ ] Validated derived-signal API and storage policy.
- [ ] Explainable visual scoring and distraction tests.
- [ ] Privacy and fairness review.

