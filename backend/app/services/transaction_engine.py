from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


class TransactionRuleError(ValueError):
    pass


def validate_transaction_account(account: Account, tx_type: str) -> None:
    if tx_type == "income" and account.type not in ["cash", "bank"]:
        raise TransactionRuleError("Income transaction must use a cash or bank account.")

    if tx_type == "expense" and account.type not in ["cash", "bank"]:
        raise TransactionRuleError("Expense transaction must use a cash or bank account.")

    if tx_type == "card_spend" and account.type != "credit_card":
        raise TransactionRuleError("Card spend transaction must use a credit card account.")


def apply_balance_change(account: Account, tx_type: str, amount: Decimal) -> None:
    if tx_type == "income":
        account.current_balance = Decimal(account.current_balance) + amount
    elif tx_type == "expense":
        account.current_balance = Decimal(account.current_balance) - amount
    elif tx_type == "card_spend":
        pass


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    account = db.query(Account).filter(Account.id == payload.account_id).first()
    if not account:
        raise TransactionRuleError("Account not found.")

    if account.user_id != payload.user_id:
        raise TransactionRuleError("Account does not belong to the user.")

    validate_transaction_account(account, payload.type.value)

    amount = Decimal(payload.amount)
    if amount <= 0:
        raise TransactionRuleError("Amount must be greater than 0.")

    tx = Transaction(
        user_id=payload.user_id,
        account_id=payload.account_id,
        type=payload.type.value,
        amount=amount,
        note=payload.note,
        description=payload.description
    )

    apply_balance_change(account, payload.type.value, amount)

    db.add(tx)
    db.add(account)
    db.commit()
    db.refresh(tx)
    return tx