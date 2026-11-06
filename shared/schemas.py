from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
    question: str
    answer: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str

class KeyPoints(BaseModel):
    key_points: List[str]

class Summary(BaseModel):
    short_summary: str
    detailed_summary: str

class LearningMaterials(BaseModel):
    summary: Summary
    key_points: KeyPoints
    flashcards: List[Flashcard]
    quiz: List[QuizQuestion]