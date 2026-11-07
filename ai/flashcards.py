import ollama, json
from pydantic import BaseModel
from typing import List
from ai.prompts import FLASHCARD_PROMPT

class Flashcard(BaseModel):
    question: str
    answer: str
class FlashcardList(BaseModel):
    flashcards: List[Flashcard]

def generate_flashcards(transcript_text: str, count: int = 5) -> dict:
    prompt = FLASHCARD_PROMPT.format(transcript=transcript_text, count=count)
    response = ollama.chat(model='qwen2.5', messages=[{'role': 'user', 'content': prompt}], format='json')
    raw_json = json.loads(response['message']['content'])
    return FlashcardList(**raw_json).model_dump()