"""
SkillExtractionTool
───────────────────
Identifies and categorises skills from resume text:
  • Technical skills
  • Soft skills
  • Tools
  • Programming languages
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


SKILL_PROMPT = """You are an expert skill extractor. Analyse the following resume text
and categorise ALL skills into four buckets. Return ONLY valid JSON:

{{
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "tools": ["tool1", "tool2"],
  "programming_languages": ["lang1", "lang2"]
}}

Rules:
- Extract explicitly mentioned AND implied skills.
- Do NOT invent skills that cannot be inferred from the text.
- Return ONLY the JSON, no markdown fences, no extra text.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""


class SkillExtractionTool(BaseTool):
    name: str = "SkillExtractionTool"
    description: str = (
        "Analyzes resume text and extracts categorised skills: "
        "technical, soft, tools, and programming languages."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        prompt = SKILL_PROMPT.format(resume_text=resume_text)
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
