"""
WeaknessDetectionTool
─────────────────────
Identifies resume weaknesses:
  • vague bullet points
  • missing metrics
  • unclear role impact
  • missing skills
  • inconsistent formatting
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


WEAKNESS_PROMPT = """You are a professional resume critic. Analyse the resume below and
find ALL weaknesses. For each weakness provide:
1. The original problematic text
2. Why it is weak
3. An improved version

Return ONLY valid JSON — an array of objects:

[
  {{
    "original": "original text",
    "issue": "why it is weak",
    "improved_version": "stronger rewrite"
  }}
]

Weakness categories to check:
- Vague bullet points
- Missing measurable metrics / achievements
- Unclear role impact
- Missing important skills
- Inconsistent formatting

Rules:
- Return ONLY the JSON array, no extra text.
- Include at least the top 5 weaknesses if present.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class WeaknessDetectionTool(BaseTool):
    name: str = "WeaknessDetectionTool"
    description: str = (
        "Detects resume weaknesses such as vague bullet points, "
        "missing metrics, unclear impact, missing skills, and "
        "formatting inconsistencies."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = WEAKNESS_PROMPT.format(resume_text=resume_text)
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
