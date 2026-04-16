from fastapi import HTTPException, status
from src.schemas.error_schema import ErrorResponseSchema, FieldError


class PaymentValidationError(HTTPException):
    """
    Custom exception for payment validation errors.
    402 Payment Required for validation issues related to payment processing rules.
    """

    def __init__(self, detail: str, field: str = "payment"):
        error_response = ErrorResponseSchema(
            status="error",
            message=detail,
            errors=[FieldError(field=field, message=detail)]
        )
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=error_response.model_dump()
        )
