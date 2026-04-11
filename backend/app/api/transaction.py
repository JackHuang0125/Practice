from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_engine import create_transaction, TransactionRuleError

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
def create_transaction_api(payload: TransactionCreate, db: Session = Depends(get_db)):
    try:
        tx = create_transaction(db, payload)
        return tx
    except TransactionRuleError as e:
        raise HTTPException(status_code=400, detail=str(e))