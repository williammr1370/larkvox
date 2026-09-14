"""
Servicio de integración con ElevenLabs.
Maneja la generación de audio y consulta de voces/modelos.
"""
import time
import uuid
from pathlib import Path

import httpx

from app.config import settings


class ElevenLabsError(Exception):
    """Error específico de ElevenLabs."""
    pass


class ElevenLabsService:
    """Cliente para la API de ElevenLabs."""
    
    def __init__(self) -> None:
        self.base_url = settings.elevenlabs_base_url
        self.api_key = settings.elevenlabs_api_key
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
    
    async def generar_audio(
        self,
        texto: str,
        voice_id: str,
        model_id: str = "eleven_flash_v2_5",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
    ) -> dict:
        """
        Genera audio a partir de texto.
        
        Returns:
            dict con: audio_bytes, latencia, filename
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        payload = {
            "text": texto,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
        }
        
        inicio = time.time()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers)
                latencia = time.time() - inicio
                
                if response.status_code != 200:
                    raise ElevenLabsError(
                        f"Error {response.status_code}: {response.text[:200]}"
                    )
                
                # Guardar archivo
                filename = f"{uuid.uuid4().hex}_{voice_id[:8]}.mp3"
                filepath = settings.audio_storage_dir / filename
                filepath.write_bytes(response.content)
                
                return {
                    "audio_bytes": response.content,
                    "latencia": latencia,
                    "filename": filename,
                    "tamaño_kb": len(response.content) / 1024,
                }
                
            except httpx.RequestError as e:
                raise ElevenLabsError(f"Error de conexión: {str(e)}") from e
    
    async def listar_voces(self) -> list[dict]:
        """Obtiene la lista de voces disponibles."""
        url = f"{self.base_url}/voices"
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=self.headers)
            
            if response.status_code != 200:
                raise ElevenLabsError(f"Error {response.status_code}: {response.text[:200]}")
            
            data = response.json()
            return data.get("voices", [])
    
    async def listar_modelos(self) -> list[dict]:
        """Obtiene la lista de modelos disponibles."""
        url = f"{self.base_url}/models"
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=self.headers)
            
            if response.status_code != 200:
                raise ElevenLabsError(f"Error {response.status_code}: {response.text[:200]}")
            
            return response.json()


# Instancia singleton
elevenlabs_service = ElevenLabsService()