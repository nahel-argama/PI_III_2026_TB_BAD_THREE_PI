from pydantic import BaseModel
from src.schemas.payment.enums import PaymentMethods, PaymentStatus

class PaymentResponseDataSchema(BaseModel):
    transaction_id: str
    order_id: str
    status: PaymentStatus
    message: str
    payment_method: PaymentMethods
    currency: str
    created_at: str

class PaymentResponseSchema(BaseModel):
    success: bool
    data: PaymentResponseDataSchema