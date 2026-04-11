from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Literal["cash", "bank", "credit_card"]
    institution_name: Optional[str] = None
    current_balance: Decimal = Decimal("0.00")
    credit_limit: Optional[Decimal] = None
    statement_day: Optional[int] = None
    due_day: Optional[int] = None

    @field_validator("current_balance")
    @classmethod
    def validate_current_balance(cls, v: Decimal):
        if v < 0:
            raise ValueError("current_balance must be >= 0")
        return v

    @field_validator("credit_limit")
    @classmethod
    def validate_credit_limit(cls, v: Optional[Decimal]):
        if v is not None and v <= 0:
            raise ValueError("credit_limit must be > 0")
        return v

    @field_validator("statement_day", "due_day")
    @classmethod
    def validate_day_range(cls, v: Optional[int]):
        if v is not None and not (1 <= v <= 31):
            raise ValueError("day must be between 1 and 31")
        return v

    @model_validator(mode="after")
    def validate_credit_card_fields(self):
        if self.type == "credit_card":
            if self.credit_limit is None:
                raise ValueError("credit_limit is required for credit_card account")
            if self.statement_day is None:
                raise ValueError("statement_day is required for credit_card account")
            if self.due_day is None:
                raise ValueError("due_day is required for credit_card account")
        else:
            if self.credit_limit is not None:
                raise ValueError("credit_limit is only for credit_card account")
            if self.statement_day is not None:
                raise ValueError("statement_day is only for credit_card account")
            if self.due_day is not None:
                raise ValueError("due_day is only for credit_card account")
        return self
    
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