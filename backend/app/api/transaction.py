from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionType
from app.services.transaction_engine import create_transaction, TransactionRuleError

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
def create_transaction_api(payload: TransactionCreate, db: Session = Depends(get_db)):
    try:
        tx = create_transaction(db, payload)
        return tx
    except TransactionRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    user_id: Optional[UUID] = Query(default=None),
    account_id: Optional[UUID] = Query(default=None),
    pocket_id: Optional[UUID] = Query(default=None),
    type: Optional[TransactionType] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if user_id is not None:
        query = query.filter(Transaction.user_id == user_id)

    if account_id is not None:
        query = query.filter(Transaction.account_id == account_id)

    if pocket_id is not None:
        query = query.filter(Transaction.pocket_id == pocket_id)

    if type is not None:
        query = query.filter(Transaction.type == type.value)

    transactions = query.order_by(Transaction.created_at.desc()).all()
    return transactions