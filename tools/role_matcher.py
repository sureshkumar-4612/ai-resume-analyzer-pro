"""
RoleMatcherTool
───────────────
Infers suitable job roles from resume content and
returns match percentages.
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


ROLE_PROMPT = """You are an expert career advisor. Analyse the resume below and
infer the TOP 5 most suitable job roles for this candidate.

For each role provide a match percentage (0–100%).

Return ONLY valid JSON — an array of objects sorted by match_percentage descending:

[
  {{
    "role": "Job Title",
    "match_percentage": 87
  }}
]

Rules:
- Base the match on skills, experience, and education.
- Be realistic about match percentages.
- Return ONLY the JSON array.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class RoleMatcherTool(BaseTool):
    name: str = "RoleMatcherTool"
    description: str = (
        "Infers the top 5 suitable job roles for a candidate "
        "based on resume analysis, with match percentages."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = ROLE_PROMPT.format(resume_text=resume_text)
        result = call_llm(prompt)
        try:
            parsed = json.loads(result)
            return json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            cleaned = result.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[-1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            try:
                parsed = json.loads(cleaned.strip())
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                return result
