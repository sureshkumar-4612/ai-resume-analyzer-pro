"""
AI Resume Analyzer — Simplified & Optimized Agent
────────────────────────────────────────────────
Consolidates analysis into a single expert pass.
"""

from __future__ import annotations
import json
import time
import os
import sys

# Ensure root is in path for relative-like imports in production
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.resume_loader import ResumeLoaderTool # type: ignore
from tools.master_analysis import MasterAnalysisTool # type: ignore


class ResumeAnalyzerAgent:
    """Consolidated resume analyzer agent."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.resume_loader = ResumeLoaderTool()
        self.analysis_tool = MasterAnalysisTool()
        self.steps_log: list[dict] = []

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message, flush=True)

    def _truncate(self, text: str, limit: int) -> str:
        """Type-safe truncation for strict liners."""
        if len(text) > limit:
            return text[:limit] + "..."
        return text

    def _execute_tool(self, tool_name: str, tool, tool_input: str) -> str:
        """Execute tool and log performance."""
        self._log(f"🔧 Executing: {tool_name}...")
        start_time = time.time()
        
        try:
            result = str(tool._run(tool_input))
            status = "success" if not result.startswith("ERROR") else "error"
        except Exception as exc:
            result = f"ERROR: {exc}"
            status = "exception"

        # Safe rounding without library dependencies
        elapsed = float(int((time.time() - start_time) * 100) / 100)
        self._log(f"   ✅ {tool_name} finished in {elapsed}s")
        
        self.steps_log.append({
            "tool": tool_name,
            "status": status,
            "duration": elapsed,
            "output_preview": self._truncate(result, 200)
        })
        return result

    def run(self, file_path: str) -> dict:
        """Optimized 2-step pipeline."""
        self.steps_log = []

        # 1. Load
        raw_text = self._execute_tool("ResumeLoaderTool", self.resume_loader, file_path)
        if raw_text.startswith("ERROR"):
            return {"report": {"error": raw_text}, "steps": self.steps_log}

        # 2. Analyze
        analysis_result = self._execute_tool("MasterAnalysisTool", self.analysis_tool, raw_text)
        
        try:
            if analysis_result.startswith("ERROR"):
                raise ValueError(analysis_result)
            
            report = json.loads(analysis_result)
            return {"report": report, "steps": self.steps_log}
        except Exception:
            return {
                "report": {"error": "The AI analysis took too long or returned an invalid format. Please try a different file."},
                "steps": self.steps_log,
                "debug": self._truncate(analysis_result, 500) if 'analysis_result' in locals() else ""
            }


def run_analysis(file_path: str, verbose: bool = True) -> dict:
    """Entry point."""
    return ResumeAnalyzerAgent(verbose=verbose).run(file_path)
