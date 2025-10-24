from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class QuizRecord(Base):
    __tablename__ = 'quiz_records'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1024), nullable=False)
    url_hash = Column(String(128), nullable=False, unique=True)
    title = Column(String(512))
    summary = Column(Text)
    sections = Column(Text)
    quiz_json = Column(Text)
    related_json = Column(Text)
    raw_html = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
