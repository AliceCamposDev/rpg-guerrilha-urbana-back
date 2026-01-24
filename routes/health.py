from fastapi import APIRouter
from config import VAULT

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Endpoint de saúde para verificar o status do servidor"""
    try:
        vault_loaded = VAULT is not None
        vault_notes = len(VAULT.get_note_metadata()) if VAULT else 0

        return {
            "status": "healthy",
            "vault_loaded": vault_loaded,
            "vault_notes": vault_notes,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
