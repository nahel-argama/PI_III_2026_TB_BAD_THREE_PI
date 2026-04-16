from fastapi import APIRouter
from src.schemas import PaymentRequestSchema, PaymentResponseSchema, PaymentStatus
from src.services.payment_validators import validate_payment_rules
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post(
        "/payments",
        tags=["Payments"],
        response_model=PaymentResponseSchema,
        status_code=200,
        summary="Send a payment request",
        description="Endpoint to process a payment request. Validates according to predefined rules."
        )

async def create_payment(payload: PaymentRequestSchema):
    validate_payment_rules(payload)

    return PaymentResponseSchema(
        status=PaymentStatus.SUCCESS,
        created_at=datetime.now().isoformat()
    )
