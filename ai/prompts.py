SUMMARY_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and provide a short overview summary and a detailed comprehensive summary. 
Output ONLY valid JSON matching this exact structure, with no markdown formatting or conversational text:
{{
  "short_summary": "string",
  "detailed_summary": "string"
}}

Transcript:
{transcript}
"""

FLASHCARD_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and generate 3 flashcards for revision.
Output ONLY valid JSON matching this exact structure, with no markdown formatting or conversational text:
{{
  "flashcards": [
    {{
      "question": "string",
      "answer": "string"
    }}
  ]
}}

Transcript:
{transcript}
"""

QUIZ_PROMPT = """
You are an expert educational AI. Read the following lecture transcript and generate a 3-question multiple-choice quiz based strictly on the content.
Output ONLY valid JSON matching this exact structure, with no markdown formatting or conversational text:
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
Output ONLY valid JSON matching this exact structure, with no markdown formatting or conversational text:
{{
  "key_points": ["string", "string", "string"]
}}

Transcript:
{transcript}
"""