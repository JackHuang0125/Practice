from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.balance_engine import (
    calculate_balance_summary,
    calculate_pocket_detail,
    calculate_account_detail,
    calculate_fund_detail,
)
from app.schemas.dashboard import (
    DashboardHomeResponse,
    DashboardPocketDetailResponse,
    DashboardAccountDetailResponse,
    DashboardFundDetailResponse,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/home", response_model=DashboardHomeResponse)
def get_dashboard_home(db: Session = Depends(get_db)):
    try:
        result = calculate_balance_summary(db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pocket/{pocket_id}", response_model=DashboardPocketDetailResponse)
def get_dashboard_pocket_detail(pocket_id: UUID, db: Session = Depends(get_db)):
    try:
        result = calculate_pocket_detail(db, pocket_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/account/{account_id}", response_model=DashboardAccountDetailResponse)
def get_dashboard_account_detail(account_id: UUID, db: Session = Depends(get_db)):
    try:
        result = calculate_account_detail(db, account_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/fund/{fund_id}", response_model=DashboardFundDetailResponse)
def get_dashboard_fund_detail(fund_id: UUID, db: Session = Depends(get_db)):
    try:
        result = calculate_fund_detail(db, fund_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))