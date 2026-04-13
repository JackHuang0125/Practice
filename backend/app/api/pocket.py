from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.pocket import BudgetPocket
from app.schemas.pocket import PocketCreate, PocketUpdate, PocketResponse
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/pockets", tags=["pockets"])


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No default user found. Please create a user first.")
    return user


def get_user_pocket_or_404(db: Session, user_id, pocket_id: UUID) -> BudgetPocket:
    pocket = (
        db.query(BudgetPocket)
        .filter(
            BudgetPocket.id == pocket_id,
            BudgetPocket.user_id == user_id,
            BudgetPocket.is_active == True
        )
        .first()
    )
    if not pocket:
        raise HTTPException(status_code=404, detail="Pocket not found.")
    return pocket


@router.post("/", response_model=PocketResponse)
def create_pocket(payload: PocketCreate, db: Session = Depends(get_db)):
    user = get_default_user(db)

    pocket = BudgetPocket(
        user_id=user.id,
        name=payload.name,
        amount=payload.amount,
        spent_amount=payload.spent_amount,
    )

    db.add(pocket)
    db.commit()
    db.refresh(pocket)
    return pocket


@router.get("/", response_model=list[PocketResponse])
def get_pockets(db: Session = Depends(get_db)):
    user = get_default_user(db)
    pockets = (
        db.query(BudgetPocket)
        .filter(
            BudgetPocket.user_id == user.id,
            BudgetPocket.is_active == True
        )
        .order_by(BudgetPocket.created_at.desc())
        .all()
    )
    return pockets


@router.get("/{pocket_id}", response_model=PocketResponse)
def get_pocket(pocket_id: UUID, db: Session = Depends(get_db)):
    user = get_default_user(db)
    pocket = get_user_pocket_or_404(db, user.id, pocket_id)
    return pocket


@router.patch("/{pocket_id}", response_model=PocketResponse)
def update_pocket(pocket_id: UUID, payload: PocketUpdate, db: Session = Depends(get_db)):
    user = get_default_user(db)
    pocket = get_user_pocket_or_404(db, user.id, pocket_id)

    if payload.name is not None:
        pocket.name = payload.name
    if payload.amount is not None:
        pocket.amount = payload.amount
    if payload.spent_amount is not None:
        pocket.spent_amount = payload.spent_amount

    db.add(pocket)
    db.commit()
    db.refresh(pocket)
    return pocket


@router.delete("/{pocket_id}", response_model=MessageResponse)
def delete_pocket(pocket_id: UUID, db: Session = Depends(get_db)):
    user = get_default_user(db)
    pocket = get_user_pocket_or_404(db, user.id, pocket_id)

    pocket.is_active = False
    db.add(pocket)
    db.commit()

    return {"message": "Pocket archived successfully."}