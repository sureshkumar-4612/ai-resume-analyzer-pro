"""
ResumeParserTool
────────────────
Sends raw resume text to the LLM and extracts structured
sections: name, email, phone, skills, education, experience,
certifications, projects.
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


PARSER_PROMPT = """You are an expert resume parser. Given the raw text of a resume,
extract the following structured information and return ONLY valid JSON:

{{
  "name": "Candidate full name",
  "email": "email@example.com",
  "phone": "phone number",
  "skills": ["skill1", "skill2"],
  "education": ["degree — institution — year"],
  "experience": ["role — company — duration — description"],
  "certifications": ["certification name"],
  "projects": ["project name — description"]
}}

Rules:
- If a section is missing, return an empty list or empty string.
- Do NOT invent information; extract only what is present.
- Return ONLY the JSON object, no markdown fences, no explanation.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class ResumeParserTool(BaseTool):
    name: str = "ResumeParserTool"
    description: str = (
        "Takes raw resume text and returns structured JSON with "
        "name, email, phone, skills, education, experience, "
        "certifications, and projects."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text provided."
        prompt = PARSER_PROMPT.format(resume_text=resume_text)
        result = call_llm(prompt)
        # Attempt to validate JSON
        try:
            parsed = json.loads(result)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            # LLM may have wrapped it in markdown fences — try to extract
            cleaned = result.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            try:
                parsed = json.loads(cleaned.strip())
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                return result  # return as-is; downstream will handle
