"""
AI Resume Analyzer — Pipeline Agent
────────────────────────────────────
Orchestrates the full resume analysis pipeline following the
exact 9-step workflow specified in the requirements:

  Step 1 → ResumeLoaderTool     (load file)
  Step 2 → ResumeParserTool     (extract sections)
  Step 3 → SkillExtractionTool  (categorise skills)
  Step 4 → ResumeScoringTool    (score 0–100)
  Step 5 → ATSAnalyzerTool      (ATS check)
  Step 6 → WeaknessDetectionTool(find problems)
  Step 7 → ResumeImprovementTool(generate fixes)
  Step 8 → RoleMatcherTool      (match roles)
  Step 9 → ReportGeneratorTool  (final report)

Reasoning loop per step:
  Observe → Analyze → Plan → Execute Tool → Evaluate Result → Continue
"""

from __future__ import annotations
import json
import sys

from tools.resume_loader import ResumeLoaderTool  # type: ignore[import-untyped]
from tools.resume_parser import ResumeParserTool  # type: ignore[import-untyped]
from tools.skill_extraction import SkillExtractionTool  # type: ignore[import-untyped]
from tools.resume_scoring import ResumeScoringTool  # type: ignore[import-untyped]
from tools.ats_analyzer import ATSAnalyzerTool  # type: ignore[import-untyped]
from tools.weakness_detection import WeaknessDetectionTool  # type: ignore[import-untyped]
from tools.resume_improvement import ResumeImprovementTool  # type: ignore[import-untyped]
from tools.role_matcher import RoleMatcherTool  # type: ignore[import-untyped]
from tools.report_generator import ReportGeneratorTool  # type: ignore[import-untyped]


class ResumeAnalyzerAgent:
    """
    Production-grade sequential pipeline agent.

    Each step follows the Observe → Analyze → Plan → Execute → Evaluate
    reasoning pattern. If a tool returns an error, the agent retries once
    before falling back gracefully.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.resume_loader = ResumeLoaderTool()
        self.resume_parser = ResumeParserTool()
        self.skill_extractor = SkillExtractionTool()
        self.resume_scorer = ResumeScoringTool()
        self.ats_analyzer = ATSAnalyzerTool()
        self.weakness_detector = WeaknessDetectionTool()
        self.improvement_gen = ResumeImprovementTool()
        self.role_matcher = RoleMatcherTool()
        self.report_generator = ReportGeneratorTool()

        self.steps_log: list[dict] = []

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message, flush=True)

    def _execute_tool(self, tool_name: str, tool, tool_input: str, max_retries: int = 1) -> str:
        """Execute a tool with retry logic (Observe → Execute → Evaluate)."""
        self._log(f"\n{'─' * 50}")
        self._log(f"🔧 Step: {tool_name}")
        self._log(f"{'─' * 50}")

        for attempt in range(max_retries + 1):
            try:
                result = tool._run(tool_input)

                if result and result.startswith("ERROR"):
                    if attempt < max_retries:
                        self._log(f"   ⚠️  Error detected, retrying... (attempt {attempt + 2})")
                        continue
                    else:
                        self._log(f"   ❌ Tool failed after {max_retries + 1} attempts: {result[:100]}")
                else:
                    self._log(f"   ✅ {tool_name} completed successfully")

                self.steps_log.append({
                    "tool": tool_name,
                    "status": "error" if (result and result.startswith("ERROR")) else "success",
                    "output_preview": result if result else "",
                })
                return result

            except Exception as exc:
                if attempt < max_retries:
                    self._log(f"   ⚠️  Exception: {exc}, retrying...")
                    continue
                self._log(f"   ❌ Tool exception: {exc}")
                error_msg = f"ERROR: {tool_name} failed — {exc}"
                self.steps_log.append({
                    "tool": tool_name,
                    "status": "exception",
                    "output_preview": str(exc),
                })
                return error_msg

        return "ERROR: Unexpected failure"

    def run(self, file_path: str) -> dict:
        """
        Execute the full 9-step resume analysis pipeline.

        Returns a dict with:
          - report : the final structured report (dict or str)
          - steps  : list of step execution summaries
        """
        self.steps_log = []

        # ── Step 1: Input Acquisition ────────────────────────
        self._log("\n📄 STEP 1 — Input Acquisition")
        raw_text = self._execute_tool(
            "ResumeLoaderTool", self.resume_loader, file_path
        )
        if raw_text.startswith("ERROR"):
            return {"report": {"error": raw_text}, "steps": self.steps_log}

        # ── Step 2: Resume Parsing ───────────────────────────
        self._log("\n📋 STEP 2 — Resume Parsing")
        parsed_result = self._execute_tool(
            "ResumeParserTool", self.resume_parser, raw_text
        )

        # ── Step 3: Skill Extraction ─────────────────────────
        self._log("\n🎯 STEP 3 — Skill Extraction")
        skills_result = self._execute_tool(
            "SkillExtractionTool", self.skill_extractor, raw_text
        )

        # ── Step 4: Resume Scoring ───────────────────────────
        self._log("\n📊 STEP 4 — Resume Scoring")
        scoring_result = self._execute_tool(
            "ResumeScoringTool", self.resume_scorer, raw_text
        )

        # ── Step 5: ATS Compatibility Analysis ───────────────
        self._log("\n🔍 STEP 5 — ATS Compatibility Analysis")
        ats_result = self._execute_tool(
            "ATSAnalyzerTool", self.ats_analyzer, raw_text
        )

        # ── Step 6: Weakness Detection ───────────────────────
        self._log("\n⚠️  STEP 6 — Weakness Detection")
        weakness_result = self._execute_tool(
            "WeaknessDetectionTool", self.weakness_detector, raw_text
        )

        # ── Step 7: Resume Improvement Generator ─────────────
        self._log("\n💡 STEP 7 — Resume Improvement Generator")
        improvement_result = self._execute_tool(
            "ResumeImprovementTool", self.improvement_gen, raw_text
        )

        # ── Step 8: Job Role Matching ────────────────────────
        self._log("\n🎯 STEP 8 — Job Role Matching")
        role_result = self._execute_tool(
            "RoleMatcherTool", self.role_matcher, raw_text
        )

        # ── Step 9: Final Report Generation ──────────────────
        self._log("\n📝 STEP 9 — Final Report Generation")

        # Compile all analysis data for the report generator
        analysis_data = json.dumps({
            "parsed_resume": _safe_json(parsed_result),
            "skills": _safe_json(skills_result),
            "scoring": _safe_json(scoring_result),
            "ats_analysis": _safe_json(ats_result),
            "weaknesses": _safe_json(weakness_result),
            "improvements": _safe_json(improvement_result),
            "role_matches": _safe_json(role_result),
        }, indent=2)

        report_result = self._execute_tool(
            "ReportGeneratorTool", self.report_generator, analysis_data
        )

        # Try to parse the final report as JSON
        try:
            report = json.loads(report_result)
        except (json.JSONDecodeError, TypeError):
            report = report_result

        return {"report": report, "steps": self.steps_log}


def _safe_json(text: str):
    """Try to parse text as JSON; return raw string on failure."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


def run_analysis(file_path: str, verbose: bool = True) -> dict:
    """
    Convenience wrapper — creates an agent and runs the pipeline.

    Returns a dict with:
      - report : the final structured report
      - steps  : list of step execution summaries
    """
    agent = ResumeAnalyzerAgent(verbose=verbose)
    return agent.run(file_path)
