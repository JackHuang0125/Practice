from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID


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


class DashboardHomeResponse(BaseModel):
    cash_bank_balance: Decimal
    credit_card_spend: Decimal
    income_total: Decimal
    expense_total: Decimal
    spendable_balance: Decimal
    pockets: list[PocketSummary]