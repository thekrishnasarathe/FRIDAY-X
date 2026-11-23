import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.voice_routes import router as voice_router
from app.routes.chat_routes import router as chat_router
from app.routes.automation_routes import router as automation_router
from app.routes.memory_routes import router as memory_router
from app.routes.communication_routes import router as communication_router
from app.routes.coding_routes import router as coding_router
from app.routes.study_routes import router as study_router
from app.routes.security_routes import router as security_router
from app.routes.vision_routes import router as vision_router
from app.routes.file_routes import router as file_router
from app.config import APP_NAME, VERSION, OWNER_NAME, ASSISTANT_NAME, FRONTEND_URL, GROQ_API_KEY, GEMINI_API_KEY
from app.modules.memory.session_memory import get_command_history

SERVER_START_TIME = time.time()

app = FastAPI(
    title=APP_NAME,
    description=f"{ASSISTANT_NAME} — AI Powered Personal Tactical Desktop Assistant",
    version=VERSION,
)

# ─── Configure CORS ─────────────────────────────────────────
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://friday-x-nine.vercel.app",
]

env_origins = [orig.strip() for orig in FRONTEND_URL.split(",") if orig.strip()]
origins = list(dict.fromkeys(default_origins + env_origins))

if "*" in env_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ─── Register all routes ────────────────────────────────────
app.include_router(voice_router, prefix="/voice", tags=["Voice"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat API"])
app.include_router(automation_router, prefix="/automation", tags=["Automation"])
app.include_router(automation_router, prefix="/api/automation", tags=["Automation API"])
app.include_router(memory_router, prefix="/memory", tags=["Memory"])
app.include_router(memory_router, prefix="/api/memory", tags=["Memory API"])
app.include_router(communication_router, prefix="/communication", tags=["Communication"])
app.include_router(coding_router, prefix="/coding", tags=["Coding"])
app.include_router(study_router, prefix="/study", tags=["Study"])
app.include_router(security_router, prefix="/security", tags=["Security"])
app.include_router(vision_router, prefix="/vision", tags=["Vision"])
app.include_router(file_router, prefix="/files", tags=["Files"])


@app.get("/", tags=["System"])
def root():
    return {
        "message": f"{APP_NAME} Backend is running",
        "version": VERSION,
        "assistant": ASSISTANT_NAME,
        "owner": OWNER_NAME,
        "status": "online",
        "endpoints": {
            "chat": "/chat/",
            "chat_stream": "/chat/stream",
            "voice": "/voice/listen",
            "automation": "/automation/execute",
            "telemetry": "/automation/telemetry",
            "memory": "/memory/history",
            "communication": "/communication/",
            "coding": "/coding/",
            "study": "/study/",
            "security": "/security/",
            "vision": "/vision/",
            "files": "/files/",
            "docs": "/docs",
        }
    }


@app.get("/health", tags=["System"])
def health_check():
    provider = "groq" if GROQ_API_KEY else ("gemini" if GEMINI_API_KEY else "offline")
    return {
        "status": "healthy",
        "health": "ok",
        "service": APP_NAME,
        "version": VERSION,
        "llm_provider": provider,
        "llm_configured": bool(GROQ_API_KEY or GEMINI_API_KEY),
        "available_modules": [
            "voice_core", "react_agent", "stream_engine", "telemetry",
            "memory_vault", "coding_studio", "study_suite", "security_shield"
        ],
        "memory_entries": len(get_command_history(500)),
        "uptime_seconds": round(time.time() - SERVER_START_TIME, 1)
    }
