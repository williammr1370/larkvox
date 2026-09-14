"""
Modelo para guardar los resultados de las pruebas TTS.
"""
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TestResult(Base):
    """Resultado de una prueba TTS."""
    
    __tablename__ = "test_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Datos de la prueba
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    voice_id: Mapped[str] = mapped_column(String(64), nullable=False)
    voice_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_id: Mapped[str] = mapped_column(String(64), nullable=False)
    
    # Métricas
    latencia_segundos: Mapped[float] = mapped_column(Float, nullable=False)
    tamaño_kb: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Archivo generado
    audio_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    
    def __repr__(self) -> str:
        return f"<TestResult id={self.id} model={self.model_id} latencia={self.latencia_segundos:.2f}s>"