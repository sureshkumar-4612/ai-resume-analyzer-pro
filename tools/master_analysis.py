"""
MasterAnalysisTool
──────────────────
Consolidates all resume analysis steps into a single LLM call for
maximum performance and structured output.
"""

import json
from tools.base import BaseTool # type: ignore
from llm_client import call_llm # type: ignore

MASTER_PROMPT = """You are an expert career consultant and ATS (Applicant Tracking System) specialist.
Perform a comprehensive analysis of the following resume and return a structured report.

Your analysis must include:
1. Contact Information: Name and Email.
2. Resume Quality Score: A weighted score from 0-100 based on content, formatting, and impact.
3. ATS Compatibility Score: A score from 0-100 evaluating how well the resume passes automated filters.
4. Top Skills: A list of the most prominent technical and professional skills found.
5. Strengths: 2-4 key highlights of the candidate's profile.
6. Weaknesses: 2-4 areas where the resume is lacking (e.g., missing metrics, vague job descriptions).
7. Recommended Improvements: Actionable suggestions to improve the resume.
8. Suggested Roles: A list of 3-5 job roles the candidate is suited for, with a match percentage (0-100).
9. Final Verdict: A 2-3 sentence executive summary of the candidate's profile.

Return ONLY valid JSON following this schema:
{{
  "name": "Candidate Name",
  "email": "candidate@example.com",
  "resume_score": 85,
  "ats_score": 75,
  "top_skills": ["Skill 1", "Skill 2"],
  "strengths": ["Strength 1", "Strength 2"],
  "weaknesses": ["Weakness 1", "Weakness 2"],
  "recommended_improvements": ["Improvement 1", "Improvement 2"],
  "suggested_roles": [
    {{"role": "Software Engineer", "match_percentage": 90}},
    {{"role": "Data Analyst", "match_percentage": 70}}
  ],
  "final_verdict": "Executive summary here..."
}}

Rules:
- Be objective and critical.
- Ensure all scores are numbers (integers).
- Return ONLY the JSON object.

Resume text:
\"\"\"
{resume_text}
\"\"\"
"""

class MasterAnalysisTool(BaseTool):
    name: str = "MasterAnalysisTool"
    description: str = (
        "Performs a single-pass full analysis of a resume, including scoring, "
        "ATS check, skill extraction, and role matching. Returns the final report."
    )

    def _run(self, resume_text: str) -> str:
        if not resume_text or resume_text.startswith("ERROR"):
            return resume_text or "ERROR: Empty resume text."
        
        # Use simple replacement to avoid errors if resume has {} brackets
        prompt = MASTER_PROMPT.replace("{resume_text}", resume_text)
        
        try:
            result = call_llm(prompt)
        except Exception as exc:
            return f"ERROR: LLM call failed — {exc}"
        
        # ── Resilient JSON Extraction ─────────────────────────
        cleaned = result.strip()
        
        # 1. Remove Markdown code blocks if present
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
        # 2. Extract anything between first { and last }
        try:
            first_brace = cleaned.find("{")
            last_brace = cleaned.rfind("}")
            if first_brace != -1 and last_brace != -1:
                cleaned = cleaned[first_brace:last_brace+1]
                
            parsed = json.loads(cleaned)
            return json.dumps(parsed, indent=2)
        except (json.JSONDecodeError, ValueError):
            return result # Return raw if cleaning fails
