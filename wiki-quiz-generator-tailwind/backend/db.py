from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models import Base

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./quiz.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    return SessionLocal()
