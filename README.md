# AI-Powered Student Attention & Study Analytics Platform

A privacy-first study companion that helps students plan study sessions, review how they spent their time, and build consistent habits. The interface presents estimated attention, study trends, goals, and coaching suggestions in one calm dashboard.

The platform is being built in phases. **The main presentation screens currently use labeled demo data.** A separate Recorded workspace connects to an early backend for accounts, study sessions, digital engagement records, analytics, and focus-plan suggestions. Webcam-based visual attention, live AI coaching, and production rewards are planned for later phases.

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
| Recorded workspace | Registration, sign-in, recorded sessions, backend analytics, and a provisional focus plan |

The presentation screens work without a backend or webcam. Their values are fabricated to demonstrate the intended experience and are marked as demo or simulated.

## Current capabilities

- **Frontend:** React, Vite, Tailwind CSS, and Recharts; responsive navigation and interactive presentation flows.
- **Backend foundation:** FastAPI, MongoDB storage, JWT-protected accounts and profiles, owned study sessions, derived digital engagement records, client-reported potential distractions, period summaries, and an explainable focus-plan heuristic.
- **Clear data boundaries:** Digital engagement is distinct from visual attention. The backend returns unavailable visual and combined scores as `null`; it does not turn demo values into recorded measurements.

The application cannot directly measure a student's mental state or prove that looking at a screen means they understood the material. The current UI does not request camera permission or store raw webcam footage.

## Run locally

### Frontend presentation

Requires Node.js and npm. From the project root:

```bash
npm install
npm run dev
```

Open the URL printed by Vite, usually `http://localhost:5173`. To verify a production bundle, run `npm run build`.

### Recorded workspace backend

Requires Python, pip, and a running MongoDB instance. From the project root, install the backend dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

Set `MONGO_URI` and a random `JWT_SECRET` of at least 32 characters in your environment. `backend/.env.example` lists the available settings; the app reads environment variables and does not automatically load that file. Then start the API **from `backend/`**:

```bash
cd backend
uvicorn app.main:app --reload
```

Open the frontend's **Recorded workspace** screen to register or sign in. It expects `http://127.0.0.1:8000` by default; set `VITE_API_BASE_URL` before starting Vite if your API uses another address. The JWT stays in browser memory and is cleared on reload. The other screens remain presentation demos.

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

Run `python -m pip install -r backend/requirements-dev.txt`, then `python -m pytest -q` from `backend/`. The isolated backend suite currently passes. `npm run build` also passes. A real MongoDB run and browser interaction/responsive checks are still outstanding; see [TODO.md](TODO.md).

Phase 1 is owner-completed. **Phase 2 is active.** Computer vision, validated attention estimates, live GenAI coaching, and production gamification belong to later phases. The [development roadmap](docs/development/DEVELOPMENT_ROADMAP.md) describes the sequence, and [FlowFocus integration notes](docs/FLOWFOCUS_INTEGRATION.md) record which ideas and code were adapted.
