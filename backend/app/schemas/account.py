from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Literal["cash", "bank", "credit_card"]
    institution_name: Optional[str] = None
    current_balance: Decimal = Decimal("0.00")
    credit_limit: Optional[Decimal] = None
    statement_day: Optional[int] = None
    due_day: Optional[int] = None


class AccountResponse(BaseModel):
    id: str
    user_id: str
    name: str
    type: str
    institution_name: Optional[str]
    current_balance: Decimal
    credit_limit: Optional[Decimal]
    statement_day: Optional[int]
    due_day: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True