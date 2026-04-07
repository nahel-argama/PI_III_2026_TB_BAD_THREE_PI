from pydantic import BaseModel, EmailStr, Field

class CustomerSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=120)
    email: EmailStr