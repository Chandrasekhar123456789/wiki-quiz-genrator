from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class GeneratePayload(BaseModel):
    url: HttpUrl

class QuizItem(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizRecordOut(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    sections: List[str] = []
    quiz: List[QuizItem] = []
    related_topics: List[str] = []
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class QuizRecordList(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
