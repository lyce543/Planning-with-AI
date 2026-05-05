from sqlalchemy import Column, Integer, String
from app.database import Base

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(20), index=True)
    content = Column(String(1000))
