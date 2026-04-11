from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.balance_engine import calculate_balance_summary
from app.schemas.dashboard import DashboardHomeResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/home", response_model=DashboardHomeResponse)
def get_dashboard_home(db: Session = Depends(get_db)):
    try:
        result = calculate_balance_summary(db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))