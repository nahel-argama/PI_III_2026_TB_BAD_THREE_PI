from pydantic import BaseModel, Field
from datetime import datetime

class CardSchema(BaseModel):
    holder_name: str = Field(..., min_length=3, max_length=120)
    number: str = Field(..., min_length=13, max_length=19)
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int = Field(..., ge=datetime.now().year, le=datetime.now().year + 20)
    cvv: str = Field(..., min_length=3, max_length=4)