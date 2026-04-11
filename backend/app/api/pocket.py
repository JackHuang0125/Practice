from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.pocket import BudgetPocket
from app.schemas.pocket import PocketCreate, PocketResponse

router = APIRouter(prefix="/pockets", tags=["pockets"])


def get_default_user(db: Session) -> User:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="No default user found. Please create a user first.")
    return user


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