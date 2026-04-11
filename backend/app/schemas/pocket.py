from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class PocketCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: Decimal
    spent_amount: Decimal = Decimal("0.00")

    @field_validator("amount", "spent_amount")
    @classmethod
    def validate_amounts(cls, v: Decimal):
        if v < 0:
            raise ValueError("amount fields must be >= 0")
        return v

class PocketUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    amount: Decimal | None = None
    spent_amount: Decimal | None = None

    @field_validator("amount", "spent_amount")
    @classmethod
    def validate_optional_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError("amount fields must be >= 0")
        return v
    
class PocketResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    amount: Decimal
    spent_amount: Decimal
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True