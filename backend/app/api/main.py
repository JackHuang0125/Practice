from fastapi import FastAPI

from app.db import Base, engine
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.api.user import router as user_router
from app.api.account import router as account_router
from app.api.transaction import router as transaction_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(title="FlowPockets API")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(account_router)
app.include_router(transaction_router)
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {"message": "FlowPockets backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}