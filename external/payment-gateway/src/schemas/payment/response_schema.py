from pydantic import BaseModel
from src.schemas.payment.enums import PaymentMethods, PaymentStatus

class PaymentResponseSchema(BaseModel):
    status: PaymentStatus
    created_at: str