# MediaPipe asset provenance

The Phase 3 browser prototype uses `@mediapipe/tasks-vision` version 0.10.35, declared in `package.json`. The npm package identifies its license as Apache-2.0. Files under `public/mediapipe/wasm/` were copied without modification from that package's `wasm/` directory so the runtime loads from this application's origin.

`public/mediapipe/face_landmarker.task` was downloaded from Google's versioned [Face Landmarker float16 model](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task). SHA-256: `64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff`. It is used for on-device inference. Review the model's distribution terms separately before publishing a hosted build; the npm package license alone does not establish terms for every model asset.

The app does not send webcam frames or facial landmarks to Google or to the backend. Downloading the bundled asset happens from the app origin. Camera processing requires a supported browser and user permission.
