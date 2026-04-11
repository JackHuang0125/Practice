from uuid import UUID
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    currency: str = "TWD"

class UserResponse(BaseModel):
    id: UUID
    name: str
    currency: str

    class Config:
        from_attributes = True