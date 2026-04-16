from pydantic import BaseModel, Field, model_validator
from src.schemas.payment.credit_card.schema import CardSchema
from src.schemas.payment.enums import PaymentMethods

class PaymentRequestSchema(BaseModel):
    price: float = Field(..., gt=0, description="The amount to be paid. Must be greater than 0.")
    payment_method: PaymentMethods
    card: CardSchema | None = None

    @model_validator(mode="after")
    def validate_payment_method_requirements(self):
        if self.payment_method == PaymentMethods.CREDIT_CARD and self.card is None:
            raise ValueError("card is required when payment_method is credit_card")

        if self.payment_method != PaymentMethods.CREDIT_CARD and self.card is not None:
            raise ValueError("card should not be provided when payment_method is not credit_card")

        return self