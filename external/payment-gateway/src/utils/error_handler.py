from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.schemas.error_schema import ErrorResponseSchema, FieldError


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Custom handler for Pydantic validation errors.
    Transforms the raw Pydantic error format into a clean, structured response.
    """
    errors = []

    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"][1:])  # Skip "body"
        errors.append(
            FieldError(
                field=field_path,
                message=error["msg"],
                value=str(error.get("input", ""))
            )
        )

    error_response = ErrorResponseSchema(
        status="error",
        message="Validation error in request payload",
        errors=errors
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )
