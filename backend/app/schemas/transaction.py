from uuid import UUID
from decimal import Decimal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"
    card_spend = "card_spend"
    card_payment = "card_payment"

class TransactionCreate(BaseModel):
    user_id: UUID
    account_id: UUID
    type: TransactionType
    amount: Decimal
    note: str | None = None
    description: str | None = None

class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    account_id: UUID
    type: TransactionType
    amount: Decimal
    note: str | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True