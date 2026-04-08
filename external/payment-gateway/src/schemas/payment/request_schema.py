from pydantic import BaseModel, Field, HttpUrl, model_validator
from src.schemas.payment.credit_card.schema import CardSchema
from src.schemas.payment.customer.schema import CustomerSchema
from src.schemas.payment.enums import PaymentMethods

class PaymentRequestSchema(BaseModel):
    order_id: str = Field(..., min_length=1, max_length=100)
    currency: str = Field(..., min_length=3, max_length=3)
    payment_method: PaymentMethods
    callback_url: HttpUrl
    customer: CustomerSchema
    card: CardSchema | None = None

    @model_validator(mode="after")
    def validate_payment_method_requirements(self):
        if self.payment_method == PaymentMethods.CREDIT_CARD and self.card is None:
            raise ValueError("card is required when payment_method is credit_card")

        if self.payment_method != PaymentMethods.CREDIT_CARD and self.card is not None:
            raise ValueError("card should not be provided when payment_method is not credit_card")


        return self