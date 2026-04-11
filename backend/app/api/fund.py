from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.fund import ReserveFund
from app.schemas.fund import FundCreate, FundUpdate, FundResponse

router = APIRouter(prefix="/funds", tags=["funds"])


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No default user found. Please create a user first.")
    return user


def get_user_fund_or_404(db: Session, user_id, fund_id: UUID) -> ReserveFund:
    fund = (
        db.query(ReserveFund)
        .filter(
            ReserveFund.id == fund_id,
            ReserveFund.user_id == user_id,
            ReserveFund.is_active == True
        )
        .first()
    )
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found.")
    return fund


@router.post("/", response_model=FundResponse)
def create_fund(payload: FundCreate, db: Session = Depends(get_db)):
    user = get_default_user(db)

    fund = ReserveFund(
        user_id=user.id,
        name=payload.name,
        target_amount=payload.target_amount,
        current_amount=payload.current_amount,
        monthly_contribution=payload.monthly_contribution,
    )

    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund


@router.get("/", response_model=list[FundResponse])
def get_funds(db: Session = Depends(get_db)):
    user = get_default_user(db)
    funds = (
        db.query(ReserveFund)
        .filter(
            ReserveFund.user_id == user.id,
            ReserveFund.is_active == True
        )
        .order_by(ReserveFund.created_at.desc())
        .all()
    )
    return funds


@router.get("/{fund_id}", response_model=FundResponse)
def get_fund(fund_id: UUID, db: Session = Depends(get_db)):
    user = get_default_user(db)
    fund = get_user_fund_or_404(db, user.id, fund_id)
    return fund


@router.patch("/{fund_id}", response_model=FundResponse)
def update_fund(fund_id: UUID, payload: FundUpdate, db: Session = Depends(get_db)):
    user = get_default_user(db)
    fund = get_user_fund_or_404(db, user.id, fund_id)

    if payload.name is not None:
        fund.name = payload.name
    if payload.target_amount is not None:
        fund.target_amount = payload.target_amount
    if payload.current_amount is not None:
        fund.current_amount = payload.current_amount
    if payload.monthly_contribution is not None:
        fund.monthly_contribution = payload.monthly_contribution

    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund


@router.delete("/{fund_id}")
def delete_fund(fund_id: UUID, db: Session = Depends(get_db)):
    user = get_default_user(db)
    fund = get_user_fund_or_404(db, user.id, fund_id)

    fund.is_active = False
    db.add(fund)
    db.commit()

    return {"message": "Fund archived successfully."}