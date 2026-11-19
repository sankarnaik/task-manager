
from sqlalchemy import Column, Integer, String, Boolean, Text, Date
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")
    due_date = Column(Date, nullable=True)
    attachment = Column(String, nullable=True)
