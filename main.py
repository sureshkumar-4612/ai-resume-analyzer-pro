"""
AI Resume Analyzer Agent — CLI Entry Point
───────────────────────────────────────────
Usage:
    python main.py <resume_file_path>

Runs the full 9-step analysis pipeline and prints
the structured evaluation report.
"""

import sys
import json
import time
from agent import run_analysis  # type: ignore[import-untyped]


BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║          🤖  AI Resume Analyzer Agent  🤖                    ║
║    ─── Production-Grade Resume Evaluation System ───         ║
║    Model  : openrouter/free (OpenRouter)                     ║
║    Engine : LangChain Tool-Calling Agent                     ║
╚══════════════════════════════════════════════════════════════╝
"""


def format_report(report: dict | str) -> str:
    """Pretty-print the final report for terminal output."""
    if isinstance(report, str):
        return report

    lines: list[str] = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("         CANDIDATE EVALUATION REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"  Name           : {report.get('name', 'N/A')}")
    lines.append(f"  Email          : {report.get('email', 'N/A')}")
    lines.append("")
    lines.append(f"  Resume Score   : {report.get('resume_score', 'N/A')} / 100")
    lines.append(f"  ATS Score      : {report.get('ats_score', 'N/A')}%")
    lines.append("")

    # Top Skills
    skills = report.get("top_skills", [])
    if skills:
        lines.append("  Top Skills:")
        for s in skills:
            lines.append(f"    • {s}")
        lines.append("")

    # Strengths
    strengths = report.get("strengths", [])
    if strengths:
        lines.append("  Strengths:")
        for s in strengths:
            lines.append(f"    ✅ {s}")
        lines.append("")

    # Weaknesses
    weaknesses = report.get("weaknesses", [])
    if weaknesses:
        lines.append("  Weaknesses:")
        for w in weaknesses:
            lines.append(f"    ⚠️  {w}")
        lines.append("")

    # Improvements
    improvements = report.get("recommended_improvements", [])
    if improvements:
        lines.append("  Recommended Improvements:")
        for i in improvements:
            lines.append(f"    💡 {i}")
        lines.append("")

    # Suggested Roles
    roles = report.get("suggested_roles", [])
    if roles:
        lines.append("  Suggested Roles:")
        for r in roles:
            if isinstance(r, dict):
                lines.append(f"    🎯 {r.get('role', 'N/A')} ({r.get('match_percentage', '?')}%)")
            else:
                lines.append(f"    🎯 {r}")
        lines.append("")

    # Final Verdict
    verdict = report.get("final_verdict", "")
    if verdict:
        lines.append("  Final Verdict:")
        lines.append(f"    {verdict}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main() -> None:
    print(BANNER)

    if len(sys.argv) < 2:
        print("Usage: python main.py <resume_file_path>")
        print()
        print("Supported formats: PDF, TXT, MD")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"📄 Analysing resume: {file_path}")
    print("─" * 60)
    print()

    start = time.time()

    try:
        result = run_analysis(file_path)
    except Exception as exc:
        print(f"\n❌ Analysis failed: {exc}")
        sys.exit(1)

    elapsed = time.time() - start

    # ── Print intermediate steps ─────────────────────────────
    steps = result.get("steps", [])
    if steps:
        print()
        print("📋 Pipeline Steps Executed:")
        print("─" * 40)
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step['tool']}")
        print()

    # ── Print final report ───────────────────────────────────
    report = result.get("report", {})
    print(format_report(report))

    # ── Also save JSON report ────────────────────────────────
    report_path = "resume_report.json"
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report if isinstance(report, dict) else {"raw_output": report}, fh, indent=2)
    print(f"\n💾 Full JSON report saved to: {report_path}")
    print(f"⏱️  Total processing time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
