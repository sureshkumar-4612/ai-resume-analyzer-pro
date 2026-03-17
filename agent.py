"""
AI Resume Analyzer — Consolidated Pipeline Agent
────────────────────────────────────────────────
Orchestrates the resume analysis pipeline in two high-performance steps:
1. Load File (ResumeLoaderTool)
2. Single-Pass Expert Analysis (MasterAnalysisTool)

This refactored architecture reduces LLM round-trips from 8 to 1,
slashing processing time by up to 80% while maintaining accuracy.
"""

from __future__ import annotations
import json
import time

from tools.resume_loader import ResumeLoaderTool
from tools.master_analysis import MasterAnalysisTool


class ResumeAnalyzerAgent:
    """
    High-performance consolidated resume analyzer.
    Uses a single LLM pass to generate the entire evaluation report.
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.resume_loader = ResumeLoaderTool()
        self.analysis_tool = MasterAnalysisTool()
        self.steps_log: list[dict] = []

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message, flush=True)

    def _execute_tool(self, tool_name: str, tool, tool_input: str) -> str:
        """Execute a tool and log performance."""
        self._log(f"\n🔧 Executing: {tool_name}...")
        start_time = time.time()
        
        try:
            result = tool._run(tool_input)
            status = "success" if (result and not result.startswith("ERROR")) else "error"
        except Exception as exc:
            result = f"ERROR: {exc}"
            status = "exception"

        elapsed: float = float(round(time.time() - start_time, 2))
        self._log(f"   ✅ {tool_name} finished in {elapsed}s")
        
        self.steps_log.append({
            "tool": tool_name,
            "status": status,
            "duration": elapsed,
            "output": str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
        })
        return result

    def run(self, file_path: str) -> dict:
        """
        Run the optimized 2-step analysis pipeline.
        """
        self.steps_log = []

        # ── Step 1: Document Loading ─────────────────────────
        raw_text = self._execute_tool(
            "ResumeLoaderTool", self.resume_loader, file_path
        )
        if raw_text.startswith("ERROR"):
            return {"report": {"error": raw_text}, "steps": self.steps_log}

        # ── Step 2: Consolidated Analysis ─────────────────────
        try:
            analysis_result = self._execute_tool(
                "MasterAnalysisTool", self.analysis_tool, raw_text
            )
            
            # Final Report formatting
            report = json.loads(analysis_result)
            return {"report": report, "steps": self.steps_log}
            
        except (json.JSONDecodeError, TypeError):
            return {
                "report": {"error": "Failed to generate structured report."},
                "steps": self.steps_log,
                "raw_output": analysis_result if 'analysis_result' in locals() else ""
            }


def run_analysis(file_path: str, verbose: bool = True) -> dict:
    """Convenience wrapper for the core pipeline."""
    agent = ResumeAnalyzerAgent(verbose=verbose)
    return agent.run(file_path)
