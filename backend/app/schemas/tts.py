"""
Schemas de Pydantic para los endpoints de TTS.
"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TTSRequest(BaseModel):
    """Petición para generar audio a partir de texto."""
    
    model_config = ConfigDict(protected_namespaces=())
    
    texto: str = Field(..., min_length=1, max_length=5000, description="Texto a convertir")
    voice_id: str = Field(..., description="ID de la voz de ElevenLabs")
    voice_name: str | None = Field(None, description="Nombre legible de la voz")
    model_id: str = Field("eleven_flash_v2_5", description="Modelo de ElevenLabs")
    stability: float = Field(0.5, ge=0.0, le=1.0, description="Estabilidad de la voz")
    similarity_boost: float = Field(0.75, ge=0.0, le=1.0, description="Similitud con la voz original")
    created_by: str | None = Field(None, description="Nombre de quien hizo la prueba")


class TTSResponse(BaseModel):
    """Respuesta con los datos del audio generado."""
    
    model_config = ConfigDict(protected_namespaces=())
    
    id: int
    texto: str
    voice_id: str
    voice_name: str | None
    model_id: str
    latencia_segundos: float
    tamaño_kb: float
    audio_url: str
    created_at: datetime
    created_by: str | None


class VoiceInfo(BaseModel):
    """Información de una voz disponible."""
    
    voice_id: str
    name: str
    category: str | None = None
    labels: dict | None = None
    preview_url: str | None = None


class ModelInfo(BaseModel):
    """Información de un modelo disponible."""
    
    model_config = ConfigDict(protected_namespaces=())
    
    model_id: str
    name: str
    description: str | None = None


class TestResultOut(BaseModel):
    """Resultado de prueba para listar en el historial."""
    
    model_config = ConfigDict(
        from_attributes=True,
        protected_namespaces=(),
    )
    
    id: int
    texto: str
    voice_id: str
    voice_name: str | None
    model_id: str
    latencia_segundos: float
    tamaño_kb: float
    audio_url: str
    created_at: datetime
    created_by: str | None