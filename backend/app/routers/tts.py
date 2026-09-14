"""
Endpoints de TTS: generar audio, listar voces y modelos, historial.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import TestResult
from app.schemas import TTSRequest, TTSResponse, VoiceInfo, ModelInfo, TestResultOut
from app.services import ElevenLabsService
from app.services.elevenlabs_service import ElevenLabsError

router = APIRouter(prefix="/api/tts", tags=["TTS"])

# Instancia del servicio
_service = ElevenLabsService()


# ==================== GENERAR AUDIO ====================

@router.post("/generate", response_model=TTSResponse)
async def generar_tts(
    request: TTSRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Genera audio a partir de texto usando ElevenLabs.
    Guarda el resultado en la base de datos para el historial.
    """
    try:
        resultado = await _service.generar_audio(
            texto=request.texto,
            voice_id=request.voice_id,
            model_id=request.model_id,
            stability=request.stability,
            similarity_boost=request.similarity_boost,
        )
    except ElevenLabsError as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    # Guardar en base de datos
    test_result = TestResult(
        texto=request.texto,
        voice_id=request.voice_id,
        voice_name=request.voice_name,
        model_id=request.model_id,
        latencia_segundos=resultado["latencia"],
        tamaño_kb=resultado["tamaño_kb"],
        audio_filename=resultado["filename"],
        created_by=request.created_by,
    )
    db.add(test_result)
    await db.commit()
    await db.refresh(test_result)
    
    return TTSResponse(
        id=test_result.id,
        texto=test_result.texto,
        voice_id=test_result.voice_id,
        voice_name=test_result.voice_name,
        model_id=test_result.model_id,
        latencia_segundos=test_result.latencia_segundos,
        tamaño_kb=test_result.tamaño_kb,
        audio_url=f"/api/tts/audio/{test_result.audio_filename}",
        created_at=test_result.created_at,
        created_by=test_result.created_by,
    )


# ==================== SERVIR AUDIO ====================

@router.get("/audio/{filename}")
async def obtener_audio(filename: str):
    """Devuelve un archivo de audio generado."""
    # Sanitizar para evitar path traversal
    if "/" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido")
    
    filepath = settings.audio_storage_dir / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    
    return FileResponse(
        path=filepath,
        media_type="audio/mpeg",
        filename=filename,
    )


# ==================== VOCES Y MODELOS ====================

@router.get("/voices", response_model=list[VoiceInfo])
async def listar_voces():
    """Lista las voces disponibles en ElevenLabs."""
    try:
        voces = await _service.listar_voces()
    except ElevenLabsError as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    return [
        VoiceInfo(
            voice_id=v.get("voice_id"),
            name=v.get("name"),
            category=v.get("category"),
            labels=v.get("labels"),
            preview_url=v.get("preview_url"),
        )
        for v in voces
    ]


@router.get("/models", response_model=list[ModelInfo])
async def listar_modelos():
    """Lista los modelos disponibles en ElevenLabs."""
    try:
        modelos = await _service.listar_modelos()
    except ElevenLabsError as e:
        raise HTTPException(status_code=502, detail=str(e))
    
    return [
        ModelInfo(
            model_id=m.get("model_id"),
            name=m.get("name"),
            description=m.get("description"),
        )
        for m in modelos
    ]


# ==================== HISTORIAL ====================

@router.get("/history", response_model=list[TestResultOut])
async def obtener_historial(
    limit: int = Query(50, ge=1, le=200),
    created_by: str | None = Query(None, description="Filtrar por autor"),
    db: AsyncSession = Depends(get_db),
):
    """Devuelve el historial de pruebas TTS."""
    stmt = select(TestResult).order_by(desc(TestResult.created_at)).limit(limit)
    
    if created_by:
        stmt = stmt.where(TestResult.created_by == created_by)
    
    result = await db.execute(stmt)
    pruebas = result.scalars().all()
    
    return [
        TestResultOut(
            id=p.id,
            texto=p.texto,
            voice_id=p.voice_id,
            voice_name=p.voice_name,
            model_id=p.model_id,
            latencia_segundos=p.latencia_segundos,
            tamaño_kb=p.tamaño_kb,
            audio_url=f"/api/tts/audio/{p.audio_filename}",
            created_at=p.created_at,
            created_by=p.created_by,
        )
        for p in pruebas
    ]


@router.delete("/history/{test_id}")
async def eliminar_prueba(
    test_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Elimina una prueba del historial (y su audio)."""
    stmt = select(TestResult).where(TestResult.id == test_id)
    result = await db.execute(stmt)
    prueba = result.scalar_one_or_none()
    
    if not prueba:
        raise HTTPException(status_code=404, detail="Prueba no encontrada")
    
    # Eliminar archivo de audio
    filepath = settings.audio_storage_dir / prueba.audio_filename
    if filepath.exists():
        filepath.unlink()
    
    await db.delete(prueba)
    await db.commit()
    
    return {"status": "ok", "message": f"Prueba {test_id} eliminada"}