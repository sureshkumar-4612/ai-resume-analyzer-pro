"""
ResumeImprovementTool
─────────────────────
Generates:
 • Stronger bullet points
 • Missing skill recommendations
 • Role-specific improvements
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


IMPROVEMENT_PROMPT = """You are a senior career coach specialising in resume optimisation.
Given the resume text below, generate actionable improvements.

For each improvement provide:
1. The original text or area
2. The improved version
3. The category (one of: "bullet_point", "missing_skill", "role_specific")

Return ONLY valid JSON — an array of objects:

[
  {{
    "original": "original text or area",
    "improved": "improved version",
    "category": "bullet_point | missing_skill | role_specific"
  }}
]

Rules:
- Be specific, actionable, and professional.
- Include at least 5 improvements.
- Return ONLY the JSON array.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class ResumeImprovementTool(BaseTool):
    name: str = "ResumeImprovementTool"
    description: str = (
        "Generates improvement suggestions for a resume: stronger "
        "bullet points, missing skill recommendations, and "
        "role-specific enhancements."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = IMPROVEMENT_PROMPT.format(resume_text=resume_text)
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
