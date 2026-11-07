import ollama
import json
from shared.schemas import Summary
from ai.prompts import SUMMARY_PROMPT

def generate_summary(transcript_text: str) -> dict:
    """
    Takes a raw transcript string and returns a validated summary dictionary.
    """
    prompt = SUMMARY_PROMPT.format(transcript=transcript_text)
    
    response = ollama.chat(
        model='qwen2.5',
        messages=[{'role': 'user', 'content': prompt}],
        format='json' 
    )
    
    # Parse the string response into a JSON object
    raw_json = json.loads(response['message']['content'])
    
    # Validate against the Pydantic schema
    validated_summary = Summary(**raw_json)
    
    return validated_summary.model_dump()

# Local Test
if __name__ == "__main__":
    test_transcript = "Machine learning is a subset of artificial intelligence that allows systems to learn from data without being explicitly programmed for every task."
    print("Sending transcript to Qwen...")
    result = generate_summary(test_transcript)
    print("Success! Here is the JSON output:")
    print(json.dumps(result, indent=2))