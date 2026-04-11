from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class FundCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    target_amount: Decimal
    current_amount: Decimal = Decimal("0.00")
    monthly_contribution: Decimal = Decimal("0.00")

    @field_validator("target_amount", "current_amount", "monthly_contribution")
    @classmethod
    def validate_amounts(cls, v: Decimal):
        if v < 0:
            raise ValueError("amount fields must be >= 0")
        return v


class FundUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    monthly_contribution: Decimal | None = None

    @field_validator("target_amount", "current_amount", "monthly_contribution")
    @classmethod
    def validate_optional_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError("amount fields must be >= 0")
        return v


class FundResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    target_amount: Decimal
    current_amount: Decimal
    monthly_contribution: Decimal
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True