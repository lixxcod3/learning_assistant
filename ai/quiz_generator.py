import ollama, json
from pydantic import BaseModel
from typing import List
from shared.schemas import QuizQuestion
from ai.prompts import QUIZ_PROMPT

class QuizList(BaseModel):
    quiz: List[QuizQuestion]

def generate_quiz(transcript_text: str, count: int = 5) -> dict:
    prompt = QUIZ_PROMPT.format(transcript=transcript_text, count=count)
    response = ollama.chat(model='qwen2.5', messages=[{'role': 'user', 'content': prompt}], format='json')
    raw_json = json.loads(response['message']['content'])
    return QuizList(**raw_json).model_dump()