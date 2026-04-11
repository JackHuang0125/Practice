from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.pocket import BudgetPocket


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise ValueError("No default user found.")
    return user


def get_pocket_status(usage_ratio: Decimal) -> str:
    if usage_ratio < Decimal("0.8"):
        return "green"
    elif usage_ratio <= Decimal("1.0"):
        return "yellow"
    return "red"


def calculate_balance_summary(db: Session):
    user = get_default_user(db)

    cash_bank_balance = (
        db.query(func.coalesce(func.sum(Account.current_balance), 0))
        .filter(
            Account.user_id == user.id,
            Account.is_active == True,
            Account.type.in_(["cash", "bank"])
        )
        .scalar()
    )

    credit_card_used = (
        db.query(func.coalesce(func.sum(Account.current_balance), 0))
        .filter(
            Account.user_id == user.id,
            Account.is_active == True,
            Account.type == "credit_card"
        )
        .scalar()
    )

    income_total = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user.id,
            Transaction.type == "income"
        )
        .scalar()
    )

    expense_total = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user.id,
            Transaction.type == "expense"
        )
        .scalar()
    )

    pocket_rows = (
        db.query(BudgetPocket)
        .filter(
            BudgetPocket.user_id == user.id,
            BudgetPocket.is_active == True
        )
        .order_by(BudgetPocket.created_at.desc())
        .all()
    )

    pockets = []
    for pocket in pocket_rows:
        amount = Decimal(pocket.amount)
        spent_amount = Decimal(pocket.spent_amount)
        remaining_amount = amount - spent_amount

        if amount == 0:
            usage_ratio = Decimal("0.00")
        else:
            usage_ratio = (spent_amount / amount).quantize(Decimal("0.01"))

        pockets.append({
            "id": pocket.id,
            "name": pocket.name,
            "amount": amount,
            "spent_amount": spent_amount,
            "remaining_amount": remaining_amount,
            "usage_ratio": usage_ratio,
            "status": get_pocket_status(usage_ratio),
        })

    spendable_balance = Decimal(cash_bank_balance) - Decimal(credit_card_used)

    return {
        "cash_bank_balance": Decimal(cash_bank_balance),
        "credit_card_spend": Decimal(credit_card_used),
        "income_total": Decimal(income_total),
        "expense_total": Decimal(expense_total),
        "spendable_balance": Decimal(spendable_balance),
        "pockets": pockets,
    }