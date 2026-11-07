SUMMARY_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and provide a short overview summary and a detailed comprehensive summary. 
Output ONLY valid JSON:
{{
  "short_summary": "string",
  "detailed_summary": "string"
}}
Transcript:
{transcript}
"""

FLASHCARD_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and generate {count} flashcards for revision.
CRITICAL RULE: The 'answer' MUST be a highly concise core concept, strictly limited to 1 to 3 words maximum (e.g., "Mouth", "Neural Network", "Photosynthesis"). Do not use filler words, garbage words, or full sentences in the answer field.
Output ONLY valid JSON:
{{
  "flashcards": [
    {{
      "question": "string",
      "answer": "string (1-3 words max)"
    }}
  ]
}}
Transcript:
{transcript}
"""

QUIZ_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and generate a {count}-question multiple-choice quiz based strictly on the content.
Output ONLY valid JSON:
{{
  "quiz": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer": "string (must exactly match one of the options)",
      "explanation": "string"
    }}
  ]
}}
Transcript:
{transcript}
"""

KEY_POINTS_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and extract the most important key points.
Output ONLY valid JSON:
{{
  "key_points": ["string", "string", "string"]
}}
Transcript:
{transcript}
"""