from sqlalchemy import Integer, Boolean, Column, String, DateTime, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression
from tables import Description
from .database import Base


from pytz import timezone, utc
from datetime import datetime


KST = timezone('Asia/Seoul')
now = datetime.utcnow()


# todolist Table
class todos(Base):
    """
        title: e.target.title.value,
        description: e.target.description.value,
        completed: false, 
        time: Date()
    """
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(Text)
    completed = Column(Boolean, server_default=expression.false())
    created_at = Column(DateTime, default=utc.localize(now).astimezone(KST))
    
    @classmethod
    def get_id(cls, session: Session, _id: int):
        return session.query(todos).filter_by(id = _id).first()
    
    @classmethod
    def get_title(cls, session: Session, _title: str):
        return session.query(todos).filter(todos.title == _title).first()
    