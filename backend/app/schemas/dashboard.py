from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PocketSummary(BaseModel):
    id: UUID
    name: str
    amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    usage_ratio: Decimal
    status: str

    class Config:
        from_attributes = True


class PocketTransactionItem(BaseModel):
    id: UUID
    account_id: UUID
    type: str
    amount: Decimal
    note: str | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardPocketDetailResponse(BaseModel):
    id: UUID
    name: str
    amount: Decimal
    spent_amount: Decimal
    remaining_amount: Decimal
    usage_ratio: Decimal
    status: str
    transactions: list[PocketTransactionItem]


class DashboardHomeResponse(BaseModel):
    cash_bank_balance: Decimal
    credit_card_spend: Decimal
    income_total: Decimal
    expense_total: Decimal
    spendable_balance: Decimal
    pockets: list[PocketSummary]