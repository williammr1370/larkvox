"""
Punto de entrada de FastAPI para el Proyecto LV.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import health, tts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la app."""
    # Startup
    print("🚀 Iniciando Proyecto LV - Backend...")
    await init_db()
    print(f"✅ Base de datos inicializada: {settings.database_url}")
    print(f"📁 Storage de audio: {settings.audio_storage_dir}")
    yield
    # Shutdown
    print("👋 Cerrando Proyecto LV - Backend...")


app = FastAPI(
    title="Proyecto LV - API",
    description="Backend para pruebas de TTS con ElevenLabs",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(tts.router)


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {
        "service": "Proyecto LV - Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }