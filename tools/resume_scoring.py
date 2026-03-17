"""
ResumeScoringTool
─────────────────
Scores a resume 0–100 across five weighted categories:

  Content Quality   — 30 %
  Skills Relevance  — 20 %
  Experience Depth  — 20 %
  Formatting        — 10 %
  ATS Compatibility — 20 %
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


SCORING_PROMPT = """You are an expert resume evaluator. Score the following resume
on a 0–100 scale using EXACTLY these category weights:

| Category          | Weight |
|-------------------|--------|
| Content Quality   | 30     |
| Skills Relevance  | 20     |
| Experience Depth  | 20     |
| Formatting        | 10     |
| ATS Compatibility | 20     |

Return ONLY valid JSON:

{{
  "content_quality": <score 0-30>,
  "skills_relevance": <score 0-20>,
  "experience_depth": <score 0-20>,
  "formatting": <score 0-10>,
  "ats_compatibility": <score 0-20>,
  "total_score": <sum of above, 0-100>
}}

Rules:
- Be rigorous and fair.
- Return ONLY the JSON, no markdown, no explanation.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class ResumeScoringTool(BaseTool):
    name: str = "ResumeScoringTool"
    description: str = (
        "Scores a resume from 0–100 across Content Quality (30), "
        "Skills Relevance (20), Experience Depth (20), Formatting (10), "
        "and ATS Compatibility (20)."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = SCORING_PROMPT.format(resume_text=resume_text)
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
