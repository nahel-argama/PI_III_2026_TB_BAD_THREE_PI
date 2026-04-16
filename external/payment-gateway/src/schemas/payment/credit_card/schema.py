from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

class CardSchema(BaseModel):
    holder_name: str = Field(..., max_length=120)
    number: str = Field(..., min_length=13, max_length=19)
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=datetime.now().year, le=datetime.now().year + 20)
    cvv: str = Field(..., min_length=3, max_length=4)

    @field_validator('holder_name')
    @classmethod
    def validate_holder_name(cls, v: str) -> str:
        v = ' '.join(v.split())

        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Holder name must contain only letters')

        words = v.split()
        if len(words) < 2:
            raise ValueError('Holder name must have at least 2 words')

        return v

    @field_validator('number')
    @classmethod
    def validate_number(cls, v: str) -> str:
        v_clean = v.replace(' ', '')

        if not v_clean.isdigit():
            raise ValueError('Card number must contain only digits')

        if len(v_clean) < 13 or len(v_clean) > 16:
            raise ValueError('Card number must have between 13 and 16 digits')

        return v_clean

    @field_validator('expiry_year')
    @classmethod
    def validate_expiry_year(cls, v: int) -> int:
        now = datetime.now()
        if v < now.year:
            raise ValueError('Expiry year cannot be earlier than current year')
        return v

    @model_validator(mode='after')
    def validate_expiry_date(self):
        now = datetime.now()

        if self.expiry_year == now.year and self.expiry_month < now.month:
            raise ValueError('Expiry date cannot be earlier than current month')

        return self

    @field_validator('cvv')
    @classmethod
    def validate_cvv(cls, v: str) -> str:
        v = v.replace(' ', '')

        if not v.isdigit():
            raise ValueError('CVV must contain only numbers')

        if len(v) < 3 or len(v) > 4:
            raise ValueError('CVV must have between 3 and 4 digits')

        return v