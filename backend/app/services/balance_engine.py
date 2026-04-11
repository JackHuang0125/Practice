from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise ValueError("No default user found.")
    return user


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

    credit_card_spend = (
        db.query(func.coalesce(func.sum(Transaction.amount), 0))
        .join(Account, Transaction.account_id == Account.id)
        .filter(
            Transaction.user_id == user.id,
            Transaction.type == "card_spend",
            Account.type == "credit_card",
            Account.is_active == True
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

    spendable_balance = Decimal(cash_bank_balance) - Decimal(credit_card_spend)

    return {
        "cash_bank_balance": Decimal(cash_bank_balance),
        "credit_card_spend": Decimal(credit_card_spend),
        "income_total": Decimal(income_total),
        "expense_total": Decimal(expense_total),
        "spendable_balance": spendable_balance
    }