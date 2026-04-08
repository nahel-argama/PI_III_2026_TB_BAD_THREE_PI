from fastapi import APIRouter
from src.schemas import PaymentRequestSchema, PaymentResponseSchema, PaymentStatus
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post(
        "/payments",
        tags=["Payments"],
        response_model=PaymentResponseSchema,
        status_code=200,
        summary="Create a payment"
        )

async def create_payment(payload: PaymentRequestSchema):
    return PaymentResponseSchema(
        success=True,
        data={
            "transaction_id": str(uuid4().hex[:12]),
            "order_id": payload.order_id,
            "status": PaymentStatus.PENDING,
            "message": "Payment received and is being processed",
            "payment_method": payload.payment_method,
            "currency": payload.currency,
            "created_at": datetime.now().isoformat()
        }
    )
