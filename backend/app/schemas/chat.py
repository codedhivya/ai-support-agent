from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    session_id: str
    question: str


class SourceChunk(BaseModel):
    document: str
    chunk_index: int
    content: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceChunk]