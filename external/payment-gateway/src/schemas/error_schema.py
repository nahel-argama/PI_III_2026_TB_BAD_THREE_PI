from pydantic import BaseModel
from typing import Optional

class FieldError(BaseModel):
    field: str
    message: str
    value: Optional[str] = None

class ErrorResponseSchema(BaseModel):
    status: str = "error"
    message: str
    errors: list[FieldError] = []
