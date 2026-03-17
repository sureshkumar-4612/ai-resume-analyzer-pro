"""
ReportGeneratorTool
───────────────────
Compiles all analysis results into a structured final report.
"""

import json
from tools.base import BaseTool  # type: ignore[import-untyped]
from llm_client import call_llm  # type: ignore[import-untyped]


REPORT_PROMPT = """You are a professional report generator. You will be given multiple
analysis results from a resume evaluation pipeline. Compile them into one cohesive,
structured report.

Analysis Results:
\"\"\"
{analysis_data}
\"\"\"

Return ONLY valid JSON matching this schema:

{{
  "name": "Candidate name",
  "email": "email",
  "resume_score": <number>,
  "ats_score": <number>,
  "top_skills": ["skill1", "skill2", "skill3"],
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "recommended_improvements": ["improvement1", "improvement2"],
  "suggested_roles": [
    {{"role": "Role Name", "match_percentage": 87}}
  ],
  "final_verdict": "A concise professional summary of the candidate's resume quality."
}}

Rules:
- Consolidate all data accurately.
- The final_verdict should be 2–3 sentences summarizing overall quality.
- Return ONLY the JSON.
"""


class ReportGeneratorTool(BaseTool):
    name: str = "ReportGeneratorTool"
    description: str = (
        "Takes all analysis results (parsed resume, scores, ATS, "
        "weaknesses, improvements, roles) and compiles a structured "
        "final evaluation report."
    )

    def _run(self, analysis_data: str) -> str:
        if not analysis_data or analysis_data.startswith("ERROR"):
            return analysis_data or "ERROR: No analysis data provided."
        prompt = REPORT_PROMPT.format(analysis_data=analysis_data)
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
