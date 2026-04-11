import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False, default="TWD")

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    pockets = relationship("BudgetPocket", back_populates="user", cascade="all, delete-orphan")
    funds = relationship("ReserveFund", back_populates="user", cascade="all, delete-orphan")