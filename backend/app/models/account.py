import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    institution_name = Column(String, nullable=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    current_balance = Column(Numeric(12, 2), nullable=False, default=0)
    credit_limit = Column(Numeric(12, 2), nullable=True)
    statement_day = Column(Integer, nullable=True)
    due_day = Column(Integer, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")