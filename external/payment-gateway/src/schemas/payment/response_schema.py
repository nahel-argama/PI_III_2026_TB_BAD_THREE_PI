from pydantic import BaseModel
from src.schemas.enums import PaymentMethod, PaymentStatus

class PaymentResponseDataSchema(BaseModel):
    transaction_id: str
    order_id: str
    status: PaymentStatus
    message: str
    payment_method: PaymentMethod
    currency: str
    amount: float
    processed_at: str

class PaymentResponseSchema(BaseModel):
    success: bool
    data: PaymentResponseDataSchema