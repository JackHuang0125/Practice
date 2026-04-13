from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.pocket import BudgetPocket
from app.models.fund import ReserveFund

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
    fund_rows = (
        db.query(ReserveFund)
        .filter(
            ReserveFund.user_id == user.id,
            ReserveFund.is_active == True
        )
        .order_by(ReserveFund.created_at.desc())
        .all()
    )

    funds = []
    for fund in fund_rows:
        target_amount = Decimal(fund.target_amount)
        current_amount = Decimal(fund.current_amount)
        monthly_contribution = Decimal(fund.monthly_contribution)
        remaining_amount = target_amount - current_amount

        if target_amount == 0:
            progress_ratio = Decimal("0.00")
        else:
            progress_ratio = (current_amount / target_amount).quantize(Decimal("0.01"))

        funds.append({
            "id": fund.id,
            "name": fund.name,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "monthly_contribution": monthly_contribution,
            "remaining_amount": remaining_amount,
            "progress_ratio": progress_ratio,
        })

    spendable_balance = Decimal(cash_bank_balance) - Decimal(credit_card_used)

    return {
        "cash_bank_balance": Decimal(cash_bank_balance),
        "credit_card_spend": Decimal(credit_card_used),
        "income_total": Decimal(income_total),
        "expense_total": Decimal(expense_total),
        "spendable_balance": Decimal(spendable_balance),
        "pockets": pockets,
        "funds": funds,
    }


def calculate_pocket_detail(db: Session, pocket_id):
    user = get_default_user(db)

    pocket = (
        db.query(BudgetPocket)
        .filter(
            BudgetPocket.id == pocket_id,
            BudgetPocket.user_id == user.id,
            BudgetPocket.is_active == True
        )
        .first()
    )

    if not pocket:
        raise ValueError("Pocket not found.")

    amount = Decimal(pocket.amount)
    spent_amount = Decimal(pocket.spent_amount)
    remaining_amount = amount - spent_amount

    if amount == 0:
        usage_ratio = Decimal("0.00")
    else:
        usage_ratio = (spent_amount / amount).quantize(Decimal("0.01"))

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user.id,
            Transaction.pocket_id == pocket.id
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )

    transaction_items = []
    for tx in transactions:
        transaction_items.append({
            "id": tx.id,
            "account_id": tx.account_id,
            "type": tx.type,
            "amount": Decimal(tx.amount),
            "note": tx.note,
            "description": tx.description,
            "created_at": tx.created_at,
        })

    return {
        "id": pocket.id,
        "name": pocket.name,
        "amount": amount,
        "spent_amount": spent_amount,
        "remaining_amount": remaining_amount,
        "usage_ratio": usage_ratio,
        "status": get_pocket_status(usage_ratio),
        "transactions": transaction_items,
    }

def calculate_account_detail(db: Session, account_id):
    user = get_default_user(db)

    account = (
        db.query(Account)
        .filter(
            Account.id == account_id,
            Account.user_id == user.id,
            Account.is_active == True
        )
        .first()
    )

    if not account:
        raise ValueError("Account not found.")

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user.id,
            Transaction.account_id == account.id
        )
        .order_by(Transaction.created_at.desc())
        .all()
    )

    transaction_items = []
    for tx in transactions:
        transaction_items.append({
            "id": tx.id,
            "pocket_id": tx.pocket_id,
            "type": tx.type,
            "amount": Decimal(tx.amount),
            "note": tx.note,
            "description": tx.description,
            "created_at": tx.created_at,
        })

    available_credit = None
    if account.type == "credit_card" and account.credit_limit is not None:
        available_credit = Decimal(account.credit_limit) - Decimal(account.current_balance)

    return {
        "id": account.id,
        "name": account.name,
        "institution_name": account.institution_name,
        "type": account.type,
        "current_balance": Decimal(account.current_balance),
        "credit_limit": Decimal(account.credit_limit) if account.credit_limit is not None else None,
        "available_credit": available_credit,
        "statement_day": account.statement_day,
        "due_day": account.due_day,
        "is_active": account.is_active,
        "transactions": transaction_items,
    }