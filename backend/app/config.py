"""
Configuración centralizada del proyecto.
Carga variables de entorno con validación automática.
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ElevenLabs
    elevenlabs_api_key: str
    elevenlabs_base_url: str = "https://api.elevenlabs.io/v1"
    
    # TTS
    default_tts_model: str = "eleven_flash_v2_5"
    
    # Base de datos
    database_url: str = "sqlite+aiosqlite:///./proyecto_lv.db"
    
    # Storage
    audio_storage_path: str = "./storage/audio"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Convierte la cadena de CORS en lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    @property
    def audio_storage_dir(self) -> Path:
        """Devuelve el path de storage como Path y lo crea si no existe."""
        path = Path(self.audio_storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Instancia única (singleton) de configuración
settings = Settings()