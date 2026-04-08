from fastapi import APIRouter
from src.api.routes import HealthRoute, PaymentsRoute


api_router = APIRouter()
api_router.include_router(HealthRoute)
api_router.include_router(PaymentsRoute)