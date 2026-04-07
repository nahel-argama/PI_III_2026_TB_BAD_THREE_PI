from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "service": "fake-payment-gateway",
        "timestamp": datetime.now().isoformat()
    }