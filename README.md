# FRIDAY-X 🚀

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Groq](https://img.shields.io/badge/AI-Groq%20Cloud-F55036?logo=groq&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**FRIDAY-X** is an advanced, AI-powered personal desktop assistant inspired by JARVIS and FRIDAY from the Iron Man universe. Engineered with a modular FastAPI backend and a futuristic React HUD frontend, FRIDAY-X delivers natural conversation, automation commands, voice integration, system telemetry, and contextual mode management.

---

## 🌐 Live Demo & Deployment URLs

| Service | Status | Live Link |
| :--- | :---: | :--- |
| **Frontend Dashboard (Vercel)** | 🟢 Deployed | `https://your-friday-x-frontend.vercel.app` *(Replace with your Vercel URL)* |
| **Backend API (Render)** | 🟢 Deployed | `https://your-friday-x-backend.onrender.com` *(Replace with your Render URL)* |
| **Swagger API Docs** | 🟢 Live | `https://your-friday-x-backend.onrender.com/docs` |

---

## ✨ Core Features

- **🧠 Trilingual Intelligence**: Fluently processes and replies in English, Hindi, and Hinglish. Automatically detects language context and adapts tone dynamically.
- **⚡ Ultra-Fast AI Engine**: Integrates with Groq (`llama-3.1-8b-instant`) for near-instant responses with graceful offline fallback if network or API keys are unavailable.
- **🛡️ Production Hardened & Resilient**:
  - Configurable CORS supporting dynamic production frontend URLs.
  - Error Boundaries preventing blank-screen UI crashes.
  - Cross-platform file path resolution (`/` vs `C:\`) and guarded hardware access for cloud containers.
  - 512MB RAM free-tier optimization with lazy-loaded modules and response timeouts.
- **⚙️ Comprehensive Modules**:
  - 🗣️ **Voice & Audio**: Voice transcription and text-to-speech with cloud-safe fallbacks.
  - 💻 **Coding & Study Modes**: Focused contexts for software development, debugging, and study sessions.
  - 📊 **Telemetry & Automation**: System health, battery, CPU, RAM metrics, and desktop controls.
  - 🔒 **Security Protocol**: Passphrase verification, lock down controls, and session tracking.
  - 📁 **Memory & Files**: Contextual user profile memory and file management.

---

## 🛠️ Architecture & Tech Stack

```
FRIDAY-X/
├── backend/
│   ├── app/
│   │   ├── core/         # Brain, command routing, intent classifier, response engine
│   │   ├── modules/      # Automation, coding, security, study, vision, voice
│   │   ├── routes/       # FastAPI route handlers
│   │   ├── utils/        # Logger, helpers, validators
│   │   ├── config.py     # Environment configuration & paths
│   │   └── main.py       # ASGI app entry point, CORS, and health checks
│   ├── tests/            # Automated pytest test suites
│   ├── requirements.txt  # Production dependencies with PEP 508 environment markers
│   ├── Procfile          # Render/Heroku container process definition
│   └── runtime.txt       # Python runtime version pinning
├── frontend/
│   ├── src/
│   │   ├── components/   # HUD panels, ErrorBoundary, VoiceOrb, SystemStatus
│   │   ├── pages/        # Dashboard view
│   │   ├── services/     # Axios API client with dynamic VITE_API_URL
│   │   └── main.jsx      # React root wrapped in ErrorBoundary
│   ├── vercel.json       # SPA rewrite configuration
│   └── package.json      # React 19 + Vite dependencies
├── render.yaml           # 1-Click Render infrastructure blueprint
└── vercel.json           # Root Vercel monorepo configuration
```

---

## 🔑 Environment Variables

| Variable | Required | Default | Description |
| :--- | :---: | :---: | :--- |
| `OWNER_NAME` | No | `Boss` | The name or title FRIDAY uses to address you. |
| `GROQ_API_KEY` | Recommended | `""` | Free API key from [Groq Console](https://console.groq.com/) for LLM inference. |
| `GEMINI_API_KEY` | Optional | `""` | Google Gemini API key for advanced vision & OCR features. |
| `FRONTEND_URL` | Optional | `http://localhost:5173` | Allowed CORS origin (e.g. `https://your-app.vercel.app` or `*`). |
| `EMAIL_ADDRESS` | Optional | `""` | Gmail address for automated email sending. |
| `EMAIL_APP_PASSWORD` | Optional | `""` | Gmail App Password for SMTP authentication. |
| `PORT` | Optional | `8000` | Port for the backend API server (auto-injected on Render). |
| `VITE_API_URL` | Frontend | `http://localhost:8000` | Backend API URL used by the React frontend client. |

---

## 🚀 Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or pnpm

### 1. Backend Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd FRIDAY-X

# Set up Python virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env

# Run FastAPI backend with hot-reload
uvicorn app.main:app --reload --port 8000
```
Backend API will be running on `http://localhost:8000`. Test the health endpoint at `http://localhost:8000/health` or open interactive Swagger docs at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🧪 Automated Testing & Verification

Run the automated test suite and production build checks:

```bash
# Run backend pytest suite
pytest backend/tests/ -v

# Run frontend production build
cd frontend
npm run build
```

---

## ☁️ $0 Free-Tier Deployment Guide

### Deploy Backend to Render (Free)
1. Push your repository to GitHub.
2. Sign in to [Render](https://render.com/).
3. Click **New +** → **Blueprint**, select your GitHub repository, and Render will automatically read `render.yaml`.
   *Alternatively*, choose **New Web Service**:
   - **Root Directory**: leave empty (or `backend`)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir backend`
4. Add Environment Variables in the Render dashboard:
   - `GROQ_API_KEY` = your Groq API key
   - `OWNER_NAME` = `Boss`
   - `FRONTEND_URL` = your Vercel URL (e.g. `https://your-frontend.vercel.app`)
5. Click **Deploy Web Service** and note your live URL (e.g., `https://friday-x-backend.onrender.com`).

### Deploy Frontend to Vercel (Free)
1. Sign in to [Vercel](https://vercel.com/).
2. Click **Add New Project** and import your GitHub repository.
3. In **Project Settings**:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. In **Environment Variables**, add:
   - `VITE_API_URL` = `https://your-friday-x-backend.onrender.com`
5. Click **Deploy**. Your dashboard will be live with full client-side routing and automatic reconnect guards!

---

*Built with ❤️ for a production-grade personal assistant experience. "Always at your service, Boss."*
