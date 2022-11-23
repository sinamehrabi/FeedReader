from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.database import Base
from src.utils import get_current_datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=get_current_datetime)
    updated_at = Column(DateTime, nullable=True, onupdate=get_current_datetime)
