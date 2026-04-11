import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class ReserveFund(Base):
    __tablename__ = "reserve_funds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False, default=0)
    current_amount = Column(Numeric(12, 2), nullable=False, default=0)
    monthly_contribution = Column(Numeric(12, 2), nullable=False, default=0)

    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="funds")