"""
ATSAnalyzerTool
───────────────
Evaluates whether a resume is optimised for
Applicant Tracking Systems.

Checks:
 • keyword density
 • formatting simplicity
 • section labeling
 • bullet usage
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


ATS_PROMPT = """You are an ATS (Applicant Tracking System) compatibility expert.
Analyse the following resume and evaluate its ATS friendliness.

Check:
- Keyword density (are industry keywords present and well-distributed?)
- Formatting simplicity (no tables, columns, images, or unusual characters?)
- Section labeling (clear section headings like Education, Experience, Skills?)
- Bullet usage (are accomplishments listed as crisp bullet points?)

Return ONLY valid JSON:

{{
  "ats_score": <percentage 0-100>,
  "issues": [
    "issue description 1",
    "issue description 2"
  ]
}}

Rules:
- Be specific about detected issues.
- Return ONLY the JSON, no extra text.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class ATSAnalyzerTool(BaseTool):
    name: str = "ATSAnalyzerTool"
    description: str = (
        "Evaluates ATS compatibility of a resume, checking keyword density, "
        "formatting, section labeling, and bullet usage. Returns score + issues."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = ATS_PROMPT.format(resume_text=resume_text)
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
