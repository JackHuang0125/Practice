import uuid
from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    pocket_id = Column(UUID(as_uuid=True), ForeignKey("budget_pockets.id"), nullable=True)

    type = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    note = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    pocket = relationship("BudgetPocket", back_populates="transactions")