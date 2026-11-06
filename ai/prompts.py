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