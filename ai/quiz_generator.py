import ollama
import json
from pydantic import BaseModel
from typing import List
from shared.schemas import QuizQuestion
from ai.prompts import QUIZ_PROMPT

# Create a temporary wrapper to validate the list of quiz questions
class QuizList(BaseModel):
    quiz: List[QuizQuestion]

def generate_quiz(transcript_text: str) -> dict:
    """
    Takes a raw transcript string and returns a validated dictionary of quiz questions.
    """
    prompt = QUIZ_PROMPT.format(transcript=transcript_text)
    
    response = ollama.chat(
        model='qwen2.5',
        messages=[{'role': 'user', 'content': prompt}],
        format='json' 
    )
    
    # Parse and validate the JSON
    raw_json = json.loads(response['message']['content'])
    validated_quiz = QuizList(**raw_json)
    
    return validated_quiz.model_dump()

# Local Test
if __name__ == "__main__":
    test_transcript = "Machine learning is a subset of artificial intelligence that allows systems to learn from data without being explicitly programmed for every task. Deep learning is a further subset that uses neural networks with multiple layers."
    print("Generating quiz...")
    result = generate_quiz(test_transcript)
    print("Success! Here is your quiz:")
    print(json.dumps(result, indent=2))