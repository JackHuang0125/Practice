from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate, AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No default user found. Please create a user first."
        )
    return user


@router.post("/", response_model=AccountResponse)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    try:
        user = get_default_user(db)

        account = Account(
            user_id=user.id,
            name=payload.name,
            type=payload.type,
            institution_name=payload.institution_name,
            current_balance=payload.current_balance,
            credit_limit=payload.credit_limit,
            statement_day=payload.statement_day,
            due_day=payload.due_day,
        )

        db.add(account)
        db.commit()
        db.refresh(account)
        return account
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    user = get_default_user(db)
    accounts = (
        db.query(Account)
        .filter(Account.user_id == user.id, Account.is_active == True)
        .all()
    )
    return accounts


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: UUID, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=404, detail="Account not found.")

    return account