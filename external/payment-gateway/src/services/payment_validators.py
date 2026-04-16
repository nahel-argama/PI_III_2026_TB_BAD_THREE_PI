from src.schemas.payment.enums import PaymentMethods
from src.schemas.payment.exceptions import PaymentValidationError
from src.schemas.payment.request_schema import PaymentRequestSchema

def validate_payment_rules(payload: PaymentRequestSchema) -> None:

    if payload.price <= 0:
        raise PaymentValidationError("Amount must be greater than zero.", field="price")

    if payload.payment_method == PaymentMethods.CREDIT_CARD:
        if not payload.card:
            raise PaymentValidationError("Card information is required for credit card payments.", field="card")

    # error handling if credit card cvv is 000
    if payload.payment_method == PaymentMethods.CREDIT_CARD and payload.card.cvv.endswith("000"):
        raise PaymentValidationError("Invalid credit card cvv.", field="card.cvv")