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


class FundSummary(BaseModel):
    id: UUID
    name: str
    target_amount: Decimal
    current_amount: Decimal
    monthly_contribution: Decimal
    remaining_amount: Decimal
    progress_ratio: Decimal

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


class AccountTransactionItem(BaseModel):
    id: UUID
    pocket_id: UUID | None = None
    type: str
    amount: Decimal
    note: str | None = None
    description: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardAccountDetailResponse(BaseModel):
    id: UUID
    name: str
    institution_name: str | None = None
    type: str
    current_balance: Decimal
    credit_limit: Decimal | None = None
    available_credit: Decimal | None = None
    statement_day: int | None = None
    due_day: int | None = None
    is_active: bool
    transactions: list[AccountTransactionItem]


class DashboardFundDetailResponse(BaseModel):
    id: UUID
    name: str
    target_amount: Decimal
    current_amount: Decimal
    monthly_contribution: Decimal
    remaining_amount: Decimal
    progress_ratio: Decimal
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardHomeResponse(BaseModel):
    cash_bank_balance: Decimal
    credit_card_spend: Decimal
    income_total: Decimal
    expense_total: Decimal
    spendable_balance: Decimal
    pockets: list[PocketSummary]
    funds: list[FundSummary]