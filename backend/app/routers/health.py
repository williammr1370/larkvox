"""
Endpoints de health check.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Verifica que el servidor esté activo."""
    return {"status": "ok", "service": "Proyecto LV - Backend", "version": "0.1.0"}