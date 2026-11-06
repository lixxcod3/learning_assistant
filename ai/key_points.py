import ollama
import json
from shared.schemas import KeyPoints
from ai.prompts import KEY_POINTS_PROMPT

def generate_key_points(transcript_text: str) -> dict:
    """
    Takes a raw transcript string and returns a validated dictionary of key points.
    """
    prompt = KEY_POINTS_PROMPT.format(transcript=transcript_text)
    
    response = ollama.chat(
        model='qwen2.5',
        messages=[{'role': 'user', 'content': prompt}],
        format='json' 
    )
    
    # Parse and validate the JSON
    raw_json = json.loads(response['message']['content'])
    validated_key_points = KeyPoints(**raw_json)
    
    return validated_key_points.model_dump()

# Local Test
if __name__ == "__main__":
    test_transcript = "Machine learning is a subset of artificial intelligence that allows systems to learn from data without being explicitly programmed for every task. Deep learning is a further subset that uses neural networks with multiple layers."
    print("Extracting key points...")
    result = generate_key_points(test_transcript)
    print("Success! Here are your key points:")
    print(json.dumps(result, indent=2))