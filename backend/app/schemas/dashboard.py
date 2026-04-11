from decimal import Decimal
from pydantic import BaseModel


class DashboardHomeResponse(BaseModel):
    cash_bank_balance: Decimal
    credit_card_spend: Decimal
    income_total: Decimal
    expense_total: Decimal
    spendable_balance: Decimal