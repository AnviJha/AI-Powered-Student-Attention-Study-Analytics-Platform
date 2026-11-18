# AI-Powered Student Attention & Study Analytics Platform

A privacy-first study companion that helps students plan study sessions, review how they spent their time, and build consistent habits. The interface presents estimated attention, study trends, goals, and coaching suggestions in one calm dashboard.

The platform is being built in phases. **Demo mode uses labeled sample data.** Switch to Recorded data to use the backend on Dashboard, Study Session, Analytics, and Settings. An optional browser-local camera prototype is now available for active recorded sessions. Validated visual attention, live AI coaching, and production rewards are still planned work.

## What the app looks like

The responsive interface has a sidebar on desktop and a menu on mobile. Students can move between:

| Screen | What it shows |
| --- | --- |
| Dashboard | Study summary, estimated-attention trend, weekly activity, daily goal, and recent sessions |
| Study Session | Subject and topic setup, a timer, pause/resume controls, and a clearly simulated monitoring preview |
| Analytics | Daily, weekly, and monthly views of study time, estimated focus, and potential distractions |
| AI Study Coach | Sample insights and suggested study/break routines with explanations |
| Goals & Challenges | Goal progress and interactive demo challenges |
| Achievements | Example levels, XP, streaks, badges, and personal records |
| Profile & Settings | Demo preferences and the privacy explanation |
| Recorded workspace | Registration, sign-in, recorded sessions, backend analytics, provisional focus plan, and optional local camera signals |

The presentation screens work without a backend or webcam. Their values are fabricated to demonstrate the intended experience and are marked as demo or simulated.

## Current capabilities

- **Frontend:** React, Vite, Tailwind CSS, and Recharts; responsive navigation and interactive presentation flows.
- **Backend foundation:** FastAPI, MongoDB storage, JWT-protected accounts and profiles, owned study sessions, derived digital engagement records, client-reported potential distractions, period summaries, and an explainable focus-plan heuristic.
- **Optional visual prototype:** During an active recorded session, the student can opt in to browser-local MediaPipe face presence and coarse head-orientation processing. Only aggregated sample counts are sent to the backend; derived records expire after 90 days or can be deleted sooner.
- **Clear data boundaries:** The visual signal index is an unvalidated heuristic and stays separate from digital engagement. Validated visual attention and combined scores remain `null`; demo values are never turned into recorded measurements.

The application cannot directly measure a student's mental state or prove that looking at a screen means they understood the material. Camera permission is requested only after an explicit click in an active recorded session. Raw webcam footage and facial landmarks are not uploaded or stored.

## Run locally

### Frontend presentation

Requires Node.js and npm. From the project root:

```bash
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`. To verify a production bundle, run `npm run build`.

### Recorded workspace backend

Requires Python, pip, and MongoDB. From the project root, install the backend dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

For local Windows development, download the official MongoDB Community Server ZIP from [MongoDB](https://www.mongodb.com/try/download/community). The project setup used version 8.0.34. Place the ZIP at `.local/mongodb.zip`, extract it with `python backend/scripts/install_local_mongo.py`, and run the server in a separate terminal:

```bash
python backend/scripts/start_local_mongo.py
```

The server binds only to `127.0.0.1:27017` and stores its data in ignored `.local/mongo-data/`. It is not installed as a Windows service. Run `python backend/scripts/setup_local_env.py` once to create an ignored `backend/.env` containing a random JWT secret and local MongoDB URI. The backend loads this file for local development; existing process environment variables take precedence. Then start the API **from `backend/`**:

```bash
cd backend
uvicorn app.main:app --reload
```

Switch to **Recorded data** in the frontend to register or sign in. Dashboard, Study Session, Analytics, and Settings then use backend data. The other screens remain labeled presentation demos. The frontend expects `http://127.0.0.1:8000` by default; set `VITE_API_BASE_URL` before starting Vite if your API uses another address. The JWT stays in browser memory and is cleared on reload.

To try the Phase 3 prototype, start a recorded session and select **Start optional monitoring**. Your browser will ask for camera permission. MediaPipe model and WASM assets are served locally from `public/mediapipe/`; the browser performs inference on the device. Stop monitoring at any time, or delete that session's derived visual records. Camera access requires localhost or HTTPS. The index is provisional and does not appear as validated visual attention in Analytics. See the [Phase 3 guide](docs/development/PHASE_03_COMPUTER_VISION.md) for the API, limits, and evaluation still needed.

For deployment, set `MONGO_URI`, `MONGO_DB`, `JWT_SECRET`, and `CORS_ORIGINS` through the deployment environment. Use a MongoDB deployment with authentication and transport encryption. Do not deploy `backend/.env`, `.local/`, or the unauthenticated loopback development server.

## Project layout

```text
src/                   React UI, styles, mock data, and API client
backend/app/           FastAPI routes and study services
backend/tests/         Isolated backend tests
docs/development/      Phase-by-phase development guides
docs/FLOWFOCUS_INTEGRATION.md  Code provenance and integration assessment
TODO.md                Current checklist
```

FlowFocus was assessed as a group-project reference. Its selected planning and engagement concepts were adapted into this project; the temporary `/dummy` checkout has been removed and is not needed to run the app.

## Tests and development status

Run `python -m pip install -r backend/requirements-dev.txt`, then `python -m pytest -q` from `backend/`. Run `npm test` for frontend signal rules and `npm run build` for the production bundle. Run `python backend/scripts/run_real_mongo_check.py` from the project root for the real-database integration test; it uses and removes a uniquely named test database. The isolated suite currently passes (9 tests, 1 optional real-Mongo test skipped), frontend signal tests pass (2), and the build passes. Real-camera, responsive, performance, and network-privacy QA remain open. See [TODO.md](TODO.md) for the latest status.

Phase 1 is owner-completed. **Phase 2 implementation is complete, with browser acceptance checks pending. Phase 3 is active as a provisional prototype.** Validated attention estimates, live GenAI coaching, and production gamification belong to later work. The [development roadmap](docs/development/DEVELOPMENT_ROADMAP.md) describes the sequence, and [FlowFocus integration notes](docs/FLOWFOCUS_INTEGRATION.md) record which ideas and code were adapted.
