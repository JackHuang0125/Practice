from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.pocket import BudgetPocket
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate


class TransactionRuleError(ValueError):
    pass


def validate_transaction_account(account: Account, tx_type: str) -> None:
    if not account.is_active:
        raise TransactionRuleError("Account is inactive.")

    if tx_type == "income" and account.type not in ["cash", "bank"]:
        raise TransactionRuleError("Income transaction must use a cash or bank account.")

    if tx_type == "expense" and account.type not in ["cash", "bank"]:
        raise TransactionRuleError("Expense transaction must use a cash or bank account.")

    if tx_type in ["card_spend", "card_payment"] and account.type != "credit_card":
        raise TransactionRuleError(f"{tx_type} transaction must use a credit card account.")


def validate_transaction_amount(account: Account, tx_type: str, amount: Decimal) -> None:
    if amount <= 0:
        raise TransactionRuleError("Amount must be greater than 0.")

    if tx_type == "expense":
        if Decimal(account.current_balance) < amount:
            raise TransactionRuleError("Insufficient balance for expense transaction.")

    if tx_type == "card_spend":
        if account.credit_limit is None:
            raise TransactionRuleError("Credit card account missing credit_limit.")

        used_amount = Decimal(account.current_balance or 0)
        if used_amount + amount > Decimal(account.credit_limit):
            raise TransactionRuleError("Credit limit exceeded.")

    if tx_type == "card_payment":
        used_amount = Decimal(account.current_balance or 0)
        if amount > used_amount:
            raise TransactionRuleError("Card payment cannot exceed current used credit.")


def validate_pocket(db: Session, payload: TransactionCreate):
    if payload.pocket_id is None:
        return None

    if payload.type != "expense":
        raise TransactionRuleError("Only expense transactions can be assigned to a pocket.")

    pocket = (
        db.query(BudgetPocket)
        .filter(
            BudgetPocket.id == payload.pocket_id,
            BudgetPocket.user_id == payload.user_id,
            BudgetPocket.is_active == True
        )
        .first()
    )

    if not pocket:
        raise TransactionRuleError("Pocket not found.")

    return pocket


def apply_balance_change(account: Account, tx_type: str, amount: Decimal) -> None:
    if tx_type == "income":
        account.current_balance = Decimal(account.current_balance) + amount
    elif tx_type == "expense":
        account.current_balance = Decimal(account.current_balance) - amount
    elif tx_type == "card_spend":
        account.current_balance = Decimal(account.current_balance) + amount
    elif tx_type == "card_payment":
        account.current_balance = Decimal(account.current_balance) - amount


def apply_pocket_change(pocket: BudgetPocket | None, tx_type: str, amount: Decimal) -> None:
    if pocket is None:
        return

    if tx_type == "expense":
        pocket.spent_amount = Decimal(pocket.spent_amount) + amount


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    account = db.query(Account).filter(Account.id == payload.account_id).first()
    if not account:
        raise TransactionRuleError("Account not found.")

    if account.user_id != payload.user_id:
        raise TransactionRuleError("Account does not belong to the user.")

    validate_transaction_account(account, payload.type.value)

    amount = Decimal(payload.amount)
    validate_transaction_amount(account, payload.type.value, amount)

    pocket = validate_pocket(db, payload)

    tx = Transaction(
        user_id=payload.user_id,
        account_id=payload.account_id,
        pocket_id=payload.pocket_id,
        type=payload.type.value,
        amount=amount,
        note=payload.note,
        description=payload.description
    )

    apply_balance_change(account, payload.type.value, amount)
    apply_pocket_change(pocket, payload.type.value, amount)

    db.add(tx)
    db.add(account)
    if pocket is not None:
        db.add(pocket)

    db.commit()
    db.refresh(tx)
    return tx